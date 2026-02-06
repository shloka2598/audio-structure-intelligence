def infer_meter(perceived_bpm, rhythm_hierarchy):
    binary = False
    ternary = False

    for layer in rhythm_hierarchy["layers"]:
        r = layer["ratio_to_beat"]
        s = layer["strength"]

        if abs(r - 2.0) < 0.2 and s > 0.15:
            binary = True
        if abs(r - 3.0) < 0.2 and s > 0.25:
            ternary = True

    if 60 <= perceived_bpm <= 120 and binary:
        return {
            "time_signature": "4/4",
            "beats_per_bar": 4,
            "confidence": 0.85
        }

    if ternary and not binary:
        return {
            "time_signature": "3/4",
            "beats_per_bar": 3,
            "confidence": 0.8
        }

    return {
        "time_signature": "4/4",
        "beats_per_bar": 4,
        "confidence": 0.6
    }
