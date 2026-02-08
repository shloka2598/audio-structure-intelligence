"""
    Entry point for full audio structure analysis pipeline.
    Designed to be readable, deterministic, and explainable.
"""


from src.load_audio import load_audio
from src.framing import frame_signal
from src.energy import compute_rms_energy
from src.onset import detect_onsets
from src.periodicity import (
    onset_times,
    inter_onset_intervals,
    estimate_tempo,
    tempo_candidates,
    tempo_confidence,
)
from src.selection import select_perceived_tempo
from src.report import generate_report, save_report
from src.rhythm_hierarchy import build_rhythm_hierarchy
from src.groove import compute_groove_metrics
from src.tempo_drift import compute_tempo_drift
from src.meter import infer_meter
from src.sections import (
    extract_section_features,
    detect_section_boundaries,
    aggregate_section_features,
    label_sections,
)
from src.cues import generate_cues, save_cues
from src.structure import infer_structure
from src.fingerprint import (
    build_structure_fingerprint,
    save_fingerprint,
    fingerprint_to_vector,
    cluster_fingerprints,
    infer_archetype,
)
from src.visualize_structure import plot_structure_timeline
from src.visualize_density import plot_density_with_boundaries
from src.similarity import find_similar_songs
import json
import os
from src.section_similarity import (
    compare_sections,
    weighted_overall_similarity,
    explain_similarity,
    chorus_only_similarity,
    explain_chorus_similarity
)


# CONFIG
# audio_path = "audio/Perfect_Ed_Sheeran.mp3"
audio_path = "audio/Steal_My_Girl_One_Direction.mp3"
VERBOSE = False
COMPARE_MODE = True
COMPARE_CACHE = "output/compare_cache.json"

song_id = os.path.basename(audio_path)


# HELPERS
def log(msg):
    if VERBOSE:
        print(msg)


def main():
    cached_song = None
    signal, sr = load_audio(audio_path)
    duration = len(signal) / sr

    frame_size = 2048
    hop_length = 512

    frames = frame_signal(signal, frame_size, hop_length)
    energy = compute_rms_energy(frames)
    onsets = detect_onsets(energy)

    times = onset_times(onsets, hop_length, sr)
    iois = inter_onset_intervals(times)

    tempo, corr = estimate_tempo(iois)

    if not tempo:
        print("Tempo could not be estimated")
        return

    candidates = tempo_candidates(tempo)

    if VERBOSE:
        print("\nTempo estimation:")
        for t in candidates:
            conf = tempo_confidence(iois, t)
            print(f"- Candidate: {t:.2f} BPM | confidence: {conf:.3f}")

    perceived = select_perceived_tempo(candidates)

    section_features = extract_section_features(times, perceived)
    boundaries = detect_section_boundaries(section_features)
    sections = aggregate_section_features(section_features, boundaries)
    labeled_sections = label_sections(sections)

    structure = infer_structure(sections)
    cues = generate_cues(labeled_sections, duration)

    hierarchy = build_rhythm_hierarchy(
        corr=corr,
        iois=iois,
        perceived_bpm=perceived
    )

    meter = infer_meter(perceived, hierarchy)
    groove = compute_groove_metrics(times, perceived)
    tempo_drift = compute_tempo_drift(times, perceived)

    fingerprint = build_structure_fingerprint(
        song_id=song_id,
        perceived_bpm=perceived,
        meter=meter,
        structure=structure,
        labeled_sections=labeled_sections,
        duration=duration,
    )

    save_fingerprint(fingerprint)
    fp_path = "output/fingerprints.json"
    if COMPARE_MODE and os.path.exists(COMPARE_CACHE):
        with open(COMPARE_CACHE, "r") as f:
            cached_song = json.load(f)
    if os.path.exists(fp_path):
        with open(fp_path, "r") as f:
            all_fps = json.load(f)
    else:
        all_fps = []
    vec = fingerprint_to_vector(fingerprint)

    print("\nSection-level similarity:")

    for fp in all_fps:
        if fp["song_id"] == song_id:
            continue

        section_distances = compare_sections(
            labeled_sections,
            fp["sections"],
            duration,
            fp["duration"]
        )

        overall = weighted_overall_similarity(section_distances)

        if overall is None:
            continue

        print(f"\nCompared to {fp['song_id']}:")
        print(f"- Overall section similarity: {overall:.3f}")

        for label, dist in section_distances.items():
            print(f"  • {label}: {dist:.3f}")

        chorus_labels = {"chorus", "post_chorus"}

        if any(lbl in section_distances for lbl in chorus_labels):
            sa = next(s for s in labeled_sections if s["label"] in chorus_labels)
            sb = next(s for s in fp["sections"] if s["label"] in chorus_labels)

            reasons = explain_similarity(sa, sb, duration, fp["duration"])

            print("  Explanation:")
            for name, value in reasons:
                print(f"    - {name} difference: {value:.2f}")
    
    if cached_song is not None:
        print("\nChorus-only similarity:")

        chorus_scores = []

        for fp in all_fps:
            if fp["song_id"] == song_id:
                continue

            score = chorus_only_similarity(
                labeled_sections,
                fp["sections"],
                duration,
                fp["duration"]
            )

            if score is not None:
                chorus_scores.append((fp, score))

        chorus_scores.sort(key=lambda x: x[1])

        for fp, score in chorus_scores:
            print(f"- {fp['song_id']} → {score:.3f}")

            reasons = explain_chorus_similarity(
                labeled_sections,
                fp["sections"],
                duration,
                fp["duration"]
            )

            if reasons:
                print("  Reason:")
                for name, value in reasons:
                    print(f"    • {name} difference: {value:.2f}")




    # COMPARISON CACHE
    if COMPARE_MODE and not os.path.exists(COMPARE_CACHE):
        with open(COMPARE_CACHE, "w") as f:
            json.dump({
                "name": song_id,
                "archetype": infer_archetype(fingerprint),
                "sections": labeled_sections,
                "duration": duration
            }, f, indent=2)

        print("Cached first song for comparison.")
        return

    save_cues(cues)

    # PUBLIC OUTPUT

    print(f"\nSong: {song_id}")
    print(f"Perceived tempo: {perceived:.2f} BPM")
    print(f"Meter: {meter['time_signature']} ({meter['confidence']})")
    print(f"Structure: {' → '.join(s['label'] for s in structure)}")
    print(f"Archetype: {infer_archetype(fingerprint)}")

    # VERBOSE OUTPUT

    log("\nCue points:")
    for c in cues:
        log(f"- {c['time']}s → {c['type']}")

    log("\nSection boundaries:")
    for b in boundaries:
        log(f"- {b['time']}s (strength {b['strength']})")

    log("\nLabeled sections:")
    for s in labeled_sections:
        log(f"- {s['start']:.1f}s → {s['end']:.1f}s | {s['label']} | density {s['mean_density']:.2f}")

    log("\nGroove:")
    for k, v in groove.items():
        log(f"- {k}: {v}")

    if tempo_drift:
        log("\nTempo drift:")
        for k, v in tempo_drift.items():
            log(f"- {k}: {v}")

    log("\nRhythm hierarchy:")
    for l in hierarchy["layers"]:
        log(f"- {l['level']} | {l['bpm']:.2f} BPM | ratio {l['ratio_to_beat']} | strength {l['strength']}")

    # REPORT

    report = generate_report(
        duration=duration,
        sample_rate=sr,
        onsets=onsets,
        iois=iois,
        perceived_tempo=perceived,
        subdivision_tempo=max(candidates),
        conf_perceived=tempo_confidence(iois, perceived),
        conf_subdivision=tempo_confidence(iois, max(candidates)),
        rhythm_hierarchy=hierarchy,
        groove=groove,
        tempo_drift=tempo_drift,
        meter=meter,
        section_features=section_features,
        boundaries=boundaries,
        labeled_sections=labeled_sections,
        structure=structure,
        fingerprint=fingerprint
    )

    save_report(report)
    print("Analysis report saved to output/analysis.json")

    if len(all_fps) > 1:
        print("\nSimilar songs (structure-based):")

        similar = find_similar_songs(
            query_fp=fingerprint,
            all_fps=all_fps,
            top_k=5
        )
        for s in similar:
            print(f"- {s['song_id']} | distance {s['distance']}")

    # COMPARISON VISUAL

    if COMPARE_MODE and os.path.exists(COMPARE_CACHE):
        with open(COMPARE_CACHE, "r") as f:
            cached_song = json.load(f)

        if cached_song["name"] != song_id:
            from src.visualize_compare import plot_structure_comparison

            plot_structure_comparison(
                song_a={
                    "name": song_id,
                    "archetype": infer_archetype(fingerprint),
                    "sections": labeled_sections,
                    "duration": duration
                },
                song_b={
                    "name": cached_song["name"],
                    "archetype": cached_song["archetype"],
                    "sections": cached_song["sections"],
                    "duration": cached_song["duration"]
                }
            )

            os.remove(COMPARE_CACHE)

if __name__ == "__main__":
    main()
