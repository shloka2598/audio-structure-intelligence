import numpy as np

# Convert onset frame indices to time (seconds).
def onset_times(onset_frames, hop_length, sample_rate):
    return (onset_frames * hop_length) / sample_rate


# Compute inter-onset intervals (IOIs).
def inter_onset_intervals(onset_times):
    return np.diff(onset_times)


# Compute normalized autocorrelation of a 1D signal.
def autocorrelation(signal):
    signal = signal - np.mean(signal)
    corr = np.correlate(signal, signal, mode="full")
    corr = corr[corr.size // 2 :]
    return corr / np.max(corr)


#Estimate tempo from inter-onset intervals using autocorrelation.
def estimate_tempo(iois, min_bpm=40, max_bpm=200):
    if len(iois) < 2:
        return None, None

    corr = autocorrelation(iois)

    min_period = 60 / max_bpm
    max_period = 60 / min_bpm

    lag_times = np.arange(len(corr)) * np.mean(iois)

    valid = np.where((lag_times >= min_period) & (lag_times <= max_period))[0]
    if len(valid) == 0:
        return None, None

    best_lag = valid[np.argmax(corr[valid])]
    best_period = lag_times[best_lag]
    tempo_bpm = 60 / best_period

    return tempo_bpm, corr


# Generate plausible tempo candidates accounting for octave ambiguity
def tempo_candidates(tempo, min_bpm=40, max_bpm=200):
    candidates = [tempo / 2, tempo, tempo * 2]
    return [t for t in candidates if min_bpm <= t <= max_bpm]

# Estimate confidence based on IOI consistency.
def tempo_confidence(iois, tempo):
    period = 60 / tempo
    deviations = np.abs(iois - period)
    return 1.0 / (1.0 + np.mean(deviations))