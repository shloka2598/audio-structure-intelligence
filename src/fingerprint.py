import json
import os
import math

def vector_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def build_structure_fingerprint(
    song_id,
    perceived_bpm,
    meter,
    structure,
    labeled_sections,
    duration,
):
    total_time = duration

    section_times = {}
    density = {}
    groove = {}


    for s in labeled_sections:
        label = s["label"]
        length = s["end"] - s["start"]

        section_times[label] = section_times.get(label, 0) + length
        density[label] = density.get(label, []) + [s["mean_density"]]
        groove[label] = groove.get(label, []) + [s["mean_groove_std"]]

    chorus_time = section_times.get("chorus", 0)

    return {
        "song_id": song_id,
        "tempo": round(perceived_bpm, 2),
        "meter": meter["time_signature"],
        "structure": [s["label"] for s in labeled_sections],
        "sections": labeled_sections,
        "duration": duration,
        "chorus_count": sum(1 for s in labeled_sections if s["label"] == "chorus"),
        "chorus_ratio": round(chorus_time / total_time, 3),
        "avg_section_density": {
            k: round(sum(v) / len(v), 2) for k, v in density.items()
        },
        "groove_profile": {
            k: round(sum(v) / len(v), 2) for k, v in groove.items()
        }
    }



def save_fingerprint(fp, path="output/fingerprints.json"):
    import json, os

    if os.path.exists(path):
        with open(path, "r") as f:
            fps = json.load(f)
    else:
        fps = []

    fps = [f for f in fps if f.get("song_id") != fp["song_id"]]
    fps.append(fp)

    with open(path, "w") as f:
        json.dump(fps, f, indent=2)



def structure_distance(a, b):
    d_tempo = abs(a["tempo"] - b["tempo"]) / max(a["tempo"], b["tempo"])

    d_chorus = abs(a["chorus_ratio"] - b["chorus_ratio"])

    d_structure = abs(len(a["structure"]) - len(b["structure"])) / max(
        len(a["structure"]), len(b["structure"])
    )

    return round(d_tempo + d_chorus + d_structure, 3)


def fingerprint_to_vector(fp):
    tempo_norm = fp["tempo"] / 200.0
    chorus_ratio = fp["chorus_ratio"]
    structure_len = len(fp["structure"]) / 6.0

    dens = fp.get("avg_section_density", {})
    groove = fp.get("groove_profile", {})

    density_A = dens.get("post_chorus", 0.0) / 15.0
    density_B = dens.get("chorus", 0.0) / 15.0

    groove_A = groove.get("post_chorus", 0.0) / 80.0
    groove_B = groove.get("chorus", 0.0) / 80.0

    return [
        round(tempo_norm, 3),
        round(chorus_ratio, 3),
        round(structure_len, 3),
        round(density_A, 3),
        round(density_B, 3),
        round(groove_A, 3),
        round(groove_B, 3),
    ]

def cluster_fingerprints(vectors, threshold=0.25):
    clusters = []

    for v in vectors:
        placed = False
        for c in clusters:
            if vector_distance(v, c[0]) < threshold:
                c.append(v)
                placed = True
                break
        if not placed:
            clusters.append([v])

    return clusters


def infer_archetype(fp):
    if fp["chorus_ratio"] > 0.3 and len(fp["structure"]) == 3:
        return "contrast_anthem"

    if fp["chorus_ratio"] == 0.0 and len(fp["structure"]) >= 3:
        return "sustained_energy"

    if fp["chorus_ratio"] < 0.2:
        return "narrative_build"

    return "hybrid_form"