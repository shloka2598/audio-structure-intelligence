import json
import csv
import os

def generate_cues(labeled_sections, duration):
    cues = []
    last_label = None

    for i, s in enumerate(labeled_sections):
        start = round(s["start"], 2)
        end = round(s["end"], 2)
        label = s["label"]

        if i == 0:
            cues.append({
                "time": start,
                "type": "INTRO"
            })

        if label == "chorus":
            cues.append({
                "time": start,
                "type": "CHORUS_START"
            })
            cues.append({
                "time": end,
                "type": "CHORUS_END"
            })

        if label == "post_chorus" and last_label == "chorus":
            cues.append({
                "time": start,
                "type": "POST_CHORUS"
            })

        last_label = label

    cues.append({
        "time": round(duration, 2),
        "type": "OUTRO"
    })

    cues = sorted(cues, key=lambda x: (x["time"], x["type"]))
    return cues


def save_cues(cues, base_path="output"):
    os.makedirs(base_path, exist_ok=True)

    with open(f"{base_path}/cues.json", "w") as f:
        json.dump(cues, f, indent=2)

    with open(f"{base_path}/cues.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_seconds", "label"])
        for c in cues:
            writer.writerow([c["time"], c["type"]])
