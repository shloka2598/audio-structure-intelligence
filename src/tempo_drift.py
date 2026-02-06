import numpy as np


# Analyze tempo drift and push–pull over time using sliding windows
def compute_tempo_drift(onset_times, perceived_bpm, window_seconds=12):
    beat_period = 60.0 / perceived_bpm
    duration = onset_times[-1]

    windows = []
    start = 0.0

    local_bpms = []

    while start + window_seconds <= duration:
        end = start + window_seconds
        mask = (onset_times >= start) & (onset_times < end)
        window_onsets = onset_times[mask]

        if len(window_onsets) >= 3:
            beat_indices = np.round(window_onsets / beat_period)
            beat_times = beat_indices * beat_period
            deviations = window_onsets - beat_times

            mask = np.abs(deviations) < (0.15 * beat_period)
            beat_onsets = window_onsets[mask]

            if len(beat_onsets) >= 3:
                iois = np.diff(beat_onsets)
                local_period = np.median(iois)
                local_bpm = 60.0 / local_period

                if abs(local_bpm - perceived_bpm) <= 0.25 * perceived_bpm:
                    local_bpms.append(local_bpm)
                    windows.append({
                        "start": round(start, 2),
                        "end": round(end, 2),
                        "bpm": round(local_bpm, 2)
                    })

        start += window_seconds / 2

    if not local_bpms:
        return None

    local_bpms = np.array(local_bpms)

    if len(local_bpms) < 5:
        return {
            "window_seconds": window_seconds,
            "note": "Insufficient stable beat windows for global drift statistics",
            "sections": windows
        }

    drift = local_bpms - perceived_bpm

    mean_drift = float(np.mean(drift))

    bias = "neutral"
    if mean_drift > 0.5:
        bias = "push"
    elif mean_drift < -0.5:
        bias = "pull"

    return {
        "window_seconds": window_seconds,
        "mean_local_bpm": round(float(np.mean(local_bpms)), 2),
        "std_local_bpm": round(float(np.std(local_bpms)), 2),
        "max_deviation_bpm": round(float(np.max(np.abs(drift))), 2),
        "mean_deviation_bpm": round(mean_drift, 2),
        "bias": bias,
        "sections": windows
    }
