import numpy as np


def _normalize_duration(section, total_duration):
    return (section["end"] - section["start"]) / total_duration


def build_section_vector(section, total_duration):
    duration_norm = (section["end"] - section["start"]) / total_duration

    density = section.get("mean_density", 0.0) / 15.0
    groove_mean = section.get("groove_mean", 0.0) / 80.0
    groove_std = section.get("groove_std", 0.0) / 80.0

    return np.array([
        duration_norm,
        density,
        groove_mean,
        groove_std,
    ], dtype=float)



def section_distance(vec_a, vec_b):
    return float(np.linalg.norm(vec_a - vec_b))


def compare_sections(sections_a, sections_b, duration_a, duration_b):
    results = {}

    by_label_a = {}
    for s in sections_a:
        by_label_a.setdefault(s["label"], []).append(s)

    by_label_b = {}
    for s in sections_b:
        by_label_b.setdefault(s["label"], []).append(s)

    shared_labels = set(by_label_a.keys()) & set(by_label_b.keys())

    for label in shared_labels:
        dists = []

        for sa in by_label_a[label]:
            va = build_section_vector(sa, duration_a)

            for sb in by_label_b[label]:
                vb = build_section_vector(sb, duration_b)
                dists.append(section_distance(va, vb))

        if dists:
            results[label] = float(np.mean(dists))

    return results


def weighted_overall_similarity(section_distances):
    weights = {
        "chorus": 0.45,
        "post_chorus": 0.25,
        "verse": 0.2,
        "breakdown": 0.1
    }

    total = 0.0
    weight_sum = 0.0

    for label, dist in section_distances.items():
        w = weights.get(label, 0.1)
        total += w * dist
        weight_sum += w

    if weight_sum == 0:
        return None

    return min(total / weight_sum, 1.0)


def explain_similarity(section_a, section_b, duration_a, duration_b):
    va = build_section_vector(section_a, duration_a)
    vb = build_section_vector(section_b, duration_b)

    diffs = np.abs(va - vb)

    explanations = [
        ("duration shape", diffs[0]),
        ("energy density", diffs[1]),
        ("groove mean", diffs[2]),
        ("groove stability", diffs[3]),
    ]

    explanations.sort(key=lambda x: x[1], reverse=True)

    return explanations[:2]

def chorus_only_similarity(sections_a, sections_b, duration_a, duration_b):
    chorus_labels = {"chorus", "post_chorus"}

    choruses_a = [s for s in sections_a if s["label"] in chorus_labels]
    choruses_b = [s for s in sections_b if s["label"] in chorus_labels]

    if not choruses_a or not choruses_b:
        return None

    dists = []
    for sa in choruses_a:
        va = build_section_vector(sa, duration_a)
        for sb in choruses_b:
            vb = build_section_vector(sb, duration_b)
            dists.append(section_distance(va, vb))

    if not dists:
        return None

    return float(np.mean(dists))

def explain_chorus_similarity(sections_a, sections_b, duration_a, duration_b):
    chorus_labels = {"chorus", "post_chorus"}

    sa = next((s for s in sections_a if s["label"] in chorus_labels), None)
    sb = next((s for s in sections_b if s["label"] in chorus_labels), None)

    if sa is None or sb is None:
        return None

    return explain_similarity(sa, sb, duration_a, duration_b)
