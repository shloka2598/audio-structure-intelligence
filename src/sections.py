import numpy as np
from src.groove import compute_groove_metrics


def extract_section_features(onset_times, perceived_bpm, window_seconds=12):
    duration = onset_times[-1]
    start = 0.0

    features = []

    while start + window_seconds <= duration:
        end = start + window_seconds
        window_onsets = onset_times[
            (onset_times >= start) & (onset_times < end)
        ]

        if len(window_onsets) < 3:
            start += window_seconds / 2
            continue

        onset_density = len(window_onsets) / window_seconds

        groove = compute_groove_metrics(window_onsets, perceived_bpm)

        features.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "onset_density": onset_density,
            "groove_mean": groove["mean_abs_deviation_ms"],
            "groove_std": groove["std_deviation_ms"],
        })

        start += window_seconds / 2

    return features

def detect_section_boundaries(features, threshold=1.5, min_section_seconds=15):
    boundaries = []

    vectors = []
    for f in features:
        vectors.append([
            f["onset_density"],
            f["groove_mean"],
            f["groove_std"],
        ])

    vectors = np.array(vectors)

    diffs = np.linalg.norm(np.diff(vectors, axis=0), axis=1)

    mean = np.mean(diffs)
    std = np.std(diffs)

    last_boundary_time = None

    for i, d in enumerate(diffs):
        if d > mean + threshold * std:
            boundary_time = features[i]["end"]

            if last_boundary_time is not None:
                if boundary_time - last_boundary_time < min_section_seconds:
                    continue

            boundaries.append({
                "time": boundary_time,
                "strength": round(float(d), 3)
            })

            last_boundary_time = boundary_time

    return boundaries

def aggregate_section_features(features, boundaries):
    sections = []
    boundaries = [0.0] + [b["time"] for b in boundaries] + [features[-1]["end"]]

    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]

        seg = [
            f for f in features
            if f["start"] >= start and f["end"] <= end
        ]

        if not seg:
            continue

        sections.append({
            "start": start,
            "end": end,
            "mean_density": sum(f["onset_density"] for f in seg) / len(seg),
            "mean_groove_std": sum(f["groove_std"] for f in seg) / len(seg),
        })

    return sections

def label_sections(sections):
    densities = [s["mean_density"] for s in sections]
    groove_stds = [s["mean_groove_std"] for s in sections]

    d_mean = sum(densities) / len(densities)
    d_max = max(densities)
    g_mean = sum(groove_stds) / len(groove_stds)

    labeled = []

    for i, s in enumerate(sections):
        label = "post_chorus"

        if s["mean_density"] > 0.85 * d_max and s["mean_groove_std"] > g_mean:
            label = "chorus"

        elif s["mean_density"] < 0.75 * d_mean:
            label = "breakdown"

        labeled.append({
            **s,
            "label": label
        })

    return labeled
