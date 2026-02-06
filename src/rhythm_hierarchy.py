import numpy as np


# Find local maxima in autocorrelation above a relative threshold.
def find_autocorr_peaks(lag_times, corr, min_strength=0.15, min_lag=0.08):
    peaks = []
    max_corr = np.max(corr)

    for i in range(1, len(corr) - 1):
        if corr[i] > corr[i - 1] and corr[i] > corr[i + 1]:
            if corr[i] >= min_strength * max_corr and lag_times[i] >= min_lag:
                peaks.append({
                    "lag": lag_times[i],
                    "strength": float(corr[i])
                })
    return peaks


# Classify rhythmic layer based on ratio to perceived beat

def classify_layer(ratio):
    if ratio >= 4:
        return "micro"
    if 2.5 <= ratio < 4:
        return "fast_subdivision"  
    if 1.5 <= ratio < 2.5:
        return "subdivision"     
    if 0.9 <= ratio < 1.5:
        return "beat"
    if 0.6 <= ratio < 0.9:
        return "slow_pulse"    
    return "bar"


# Build a beat-anchored rhythm hierarchy.
def build_rhythm_hierarchy(
    corr,
    iois,
    perceived_bpm,
    min_bpm=10,
    max_bpm=600
):
    mean_ioi = float(np.mean(iois))
    lag_times = np.arange(len(corr)) * mean_ioi

    peaks = find_autocorr_peaks(lag_times, corr)

    layers = []
    beat_period = 60.0 / perceived_bpm

    for p in peaks:
        period = p["lag"]
        bpm = 60.0 / period

        if not (min_bpm <= bpm <= max_bpm):
            continue

        ratio = beat_period / period
        layer = classify_layer(ratio)

        layers.append({
            "level": layer,
            "bpm": round(bpm, 2),
            "period_seconds": round(period, 4),
            "strength": round(p["strength"], 3),
            "ratio_to_beat": round(ratio, 2)
        })

    unique = {}
    for l in layers:
        key = round(l["bpm"])
        if key not in unique or l["strength"] > unique[key]["strength"]:
            unique[key] = l

    layers = sorted(unique.values(), key=lambda x: x["period_seconds"])

    return {
        "reference_beat_bpm": round(perceived_bpm, 2),
        "layers": layers
    }
