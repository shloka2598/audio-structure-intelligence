import numpy as np


# Compute RMS energy for each frame
def compute_rms_energy(frames):

    energy = np.sqrt(np.mean(frames ** 2, axis=1))
    return energy
