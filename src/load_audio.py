import numpy as np
import librosa


def load_audio(path):
    """
    Load an audio file and return a normalized mono signal.

    Returns:
        signal (np.ndarray): mono audio signal in range [-1, 1]
        sr (int): sample rate
    """

    signal, sr = librosa.load(path, sr=None, mono=True)

    if signal.size == 0:
        raise ValueError("Loaded audio is empty")

    max_val = np.max(np.abs(signal))
    if max_val > 0:
        signal = signal / max_val

    return signal, sr
