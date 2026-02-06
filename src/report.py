import json


def generate_report(
    duration,
    sample_rate,
    onsets,
    iois,
    perceived_tempo,
    subdivision_tempo,
    conf_perceived,
    conf_subdivision,
    rhythm_hierarchy,
    groove,
    tempo_drift,
    meter,
    section_features,
    boundaries,
    labeled_sections,
    structure,
    fingerprint
):
    report = {
        "tempo": {
            "perceived_bpm": round(perceived_tempo, 2),
            "subdivision_bpm": round(subdivision_tempo, 2),
            "confidence": {
                "perceived": round(conf_perceived, 3),
                "subdivision": round(conf_subdivision, 3),
            },
        },
        "rhythm": {
            "num_onsets": int(len(onsets)),
            "mean_ioi_seconds": round(float(iois.mean()), 4),
        },
        "audio": {
            "duration_seconds": round(duration, 2),
            "sample_rate": sample_rate,
        },
        "explanation": {
            "summary": (
                f"Strong rhythmic subdivision detected at ~{subdivision_tempo:.1f} BPM, "
                f"with perceived beat at ~{perceived_tempo:.1f} BPM."
            ),
            "reasoning": [
                "Energy-based onset detection revealed dense rhythmic events.",
                "Autocorrelation shows strongest periodic repetition.",
                "Perceived tempo selected using human perceptual beat range (60 to 120 BPM).",
            ],
        },
        "rhythm_hierarchy": rhythm_hierarchy,
        "groove": groove,
        "tempo_drift": tempo_drift,
        "meter": meter,
        "sections": {
            "features": section_features,
            "boundaries": boundaries,
            "labeled": labeled_sections
        },
        "structure": structure,
        "fingerprint": fingerprint,
    }

    return report


def save_report(report, path="output/analysis.json"):
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
