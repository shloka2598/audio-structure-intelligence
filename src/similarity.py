import math


def section_topology_distance(fp_a, fp_b):
    seq_a = fp_a.get("structure", [])
    seq_b = fp_b.get("structure", [])

    if not seq_a or not seq_b:
        return 1.0

    len_diff = abs(len(seq_a) - len(seq_b)) / max(len(seq_a), len(seq_b))

    min_len = min(len(seq_a), len(seq_b))
    mismatch = sum(1 for i in range(min_len) if seq_a[i] != seq_b[i])
    order_penalty = mismatch / min_len if min_len > 0 else 1.0

    chorus_penalty = abs(
        fp_a.get("chorus_ratio", 0.0) - fp_b.get("chorus_ratio", 0.0)
    )

    return min(1.0, 0.5 * order_penalty + 0.3 * len_diff + 0.2 * chorus_penalty)


def energy_arc_distance(fp_a, fp_b):
    dens_a = fp_a.get("avg_section_density", {})
    dens_b = fp_b.get("avg_section_density", {})

    common = set(dens_a.keys()) & set(dens_b.keys())
    if not common:
        return 1.0

    diffs = []
    for k in common:
        a = dens_a[k]
        b = dens_b[k]
        if a > 0 and b > 0:
            diffs.append(abs(a - b) / max(a, b))

    if not diffs:
        return 1.0

    return min(1.0, sum(diffs) / len(diffs))


def tempo_meter_distance(fp_a, fp_b):
    bpm_a = fp_a.get("tempo", 0)
    bpm_b = fp_b.get("tempo", 0)

    if bpm_a <= 0 or bpm_b <= 0:
        tempo_penalty = 1.0
    else:
        tempo_penalty = abs(math.log2(bpm_a / bpm_b))

    meter_penalty = 0.0
    if fp_a.get("meter") != fp_b.get("meter"):
        meter_penalty = 0.25

    return min(1.0, tempo_penalty + meter_penalty)


def groove_distance(fp_a, fp_b):
    g_a = fp_a.get("groove_profile", {})
    g_b = fp_b.get("groove_profile", {})

    common = set(g_a.keys()) & set(g_b.keys())
    if not common:
        return 1.0

    diffs = []
    for k in common:
        a = g_a[k]
        b = g_b[k]
        if a > 0 and b > 0:
            diffs.append(abs(a - b) / max(a, b))

    if not diffs:
        return 1.0

    return min(1.0, sum(diffs) / len(diffs))


def structure_distance(fp_a, fp_b):
    return (
        0.45 * section_topology_distance(fp_a, fp_b)
        + 0.30 * energy_arc_distance(fp_a, fp_b)
        + 0.15 * tempo_meter_distance(fp_a, fp_b)
        + 0.10 * groove_distance(fp_a, fp_b)
    )


def find_similar_songs(query_fp, all_fps, top_k=5):
    results = []

    for fp in all_fps:
        if fp.get("song_id") == query_fp.get("song_id"):
            continue

        d = structure_distance(query_fp, fp)
        results.append({
            "song_id": fp.get("song_id"),
            "distance": round(float(d), 4)
        })

    results.sort(key=lambda x: x["distance"])
    return results[:top_k]
