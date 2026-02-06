import numpy as np


# Compute groove and micro-timing metrics relative to perceived beat
def compute_groove_metrics(onset_times, perceived_bpm):
    beat_period = 60.0 / perceived_bpm

    beat_indices = np.round(onset_times / beat_period)
    beat_times = beat_indices * beat_period
    deviations = onset_times - beat_times
    ratios = (onset_times / beat_period) - beat_indices
    ratios = np.abs(ratios)
    mask = (
        (np.abs(deviations) < (0.15 * beat_period)) &
        (ratios < 0.1)
    )

    deviations = deviations[mask]

    abs_dev = np.abs(deviations)

    groove = {
        "mean_abs_deviation_ms": round(float(np.mean(abs_dev) * 1000), 2),
        "std_deviation_ms": round(float(np.std(deviations) * 1000), 2),
        "max_deviation_ms": round(float(np.max(abs_dev) * 1000), 2),
    }

    iois = np.diff(onset_times)
    if len(iois) >= 4:
        even = iois[::2]
        odd = iois[1::2]
        if len(even) and len(odd):
            swing_ratio = np.mean(even) / np.mean(odd)
            groove["swing_ratio"] = round(float(swing_ratio), 3)
        else:
            groove["swing_ratio"] = None
    else:
        groove["swing_ratio"] = None

    return groove
