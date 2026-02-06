import numpy as np

# Detect onset frames based on energy increase + peak picking.
def detect_onsets(energy, threshold_ratio=1.5, min_gap=3):

    energy_diff = np.diff(energy)
    energy_diff = np.maximum(energy_diff, 0)

    threshold = threshold_ratio * np.mean(energy_diff)
    candidate_indices = np.where(energy_diff > threshold)[0]

    onsets = []
    last_onset = -min_gap

    for idx in candidate_indices:
        if idx - last_onset >= min_gap:
            onsets.append(idx)
            last_onset = idx
        else:
            if energy_diff[idx] > energy_diff[last_onset]:
                onsets[-1] = idx
                last_onset = idx

    return np.array(onsets)
