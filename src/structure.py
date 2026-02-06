def section_distance(a, b):
    d_density = abs(a["mean_density"] - b["mean_density"]) / max(a["mean_density"], b["mean_density"])
    d_groove = abs(a["mean_groove_std"] - b["mean_groove_std"]) / max(a["mean_groove_std"], b["mean_groove_std"])
    return d_density + d_groove

def infer_structure(sections, threshold=0.25):
    labels = []
    groups = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for s in sections:
        assigned = False

        for i, g in enumerate(groups):
            if section_distance(s, g[0]) < threshold:
                labels.append(alphabet[i])
                g.append(s)
                assigned = True
                break

        if not assigned:
            groups.append([s])
            labels.append(alphabet[len(groups) - 1])

    structure = []
    for s, l in zip(sections, labels):
        structure.append({
            "start": s["start"],
            "end": s["end"],
            "label": l
        })

    return structure
