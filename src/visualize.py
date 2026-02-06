import matplotlib.pyplot as plt
import numpy as np


# Plot RMS energy over time
def plot_energy(energy, hop_length, sample_rate):
    times = np.arange(len(energy)) * hop_length / sample_rate

    plt.figure(figsize=(12, 4))
    plt.plot(times, energy)
    max_time = times[-1]
    plt.xticks(np.arange(0, max_time, 10))
    plt.xlabel("Time (seconds)")
    plt.ylabel("RMS Energy")
    plt.title("Energy Over Time")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# Plot energy with onset markers
def plot_onsets(energy, onsets, hop_length, sample_rate):
    times = np.arange(len(energy)) * hop_length / sample_rate
    onset_times = onsets * hop_length / sample_rate

    max_time = times[-1]
    plt.xticks(np.arange(0, max_time, 10))
    plt.grid(True, alpha=0.3)
    plt.figure(figsize=(12, 4))
    plt.plot(times, energy, label="Energy")
    plt.vlines(onset_times, ymin=0, ymax=max(energy),
               color="r", alpha=0.3, label="Onsets")
    plt.xlabel("Time (seconds)")
    plt.ylabel("RMS Energy")
    plt.title("Energy with Detected Onsets")
    plt.legend()
    plt.tight_layout()
    plt.show()


# Plot autocorrelation of IOI's
def plot_autocorrelation(corr, iois):
    lag_times = np.arange(len(corr)) * np.mean(iois)

    plt.figure(figsize=(8, 4))
    plt.plot(lag_times, corr)
    plt.xlabel("Lag (seconds)")
    plt.ylabel("Normalized Autocorrelation")
    plt.title("Autocorrelation of Inter-Onset Intervals")
    plt.tight_layout()
    plt.show()
