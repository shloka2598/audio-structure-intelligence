import numpy as np


# Slice a 1D signal into overlapping frames.
def frame_signal(signal, frame_size, hop_length):
    signal_length = len(signal)

    if signal_length < frame_size:
        raise ValueError("Signal is shorter than one frame")

    num_frames = 1 + (signal_length - frame_size) // hop_length

    frames = np.zeros((num_frames, frame_size))

    for i in range(num_frames):
        start = i * hop_length
        end = start + frame_size
        frames[i] = signal[start:end]

    return frames
