import numpy as np
from scipy import stats

from utils.signal_proc import compute_hrv


def chrom_algorithm(rgb_signal):
    X = 3.0 * rgb_signal[:, 0] - 2.0 * rgb_signal[:, 1]
    Y = 1.5 * rgb_signal[:, 0] + rgb_signal[:, 1] - 1.5 * rgb_signal[:, 2]
    alpha = np.std(X) / (np.std(Y) + 1e-10)
    bvp = X - alpha * Y
    bvp = (bvp - np.mean(bvp)) / (np.std(bvp) + 1e-10)
    return bvp


def pos_algorithm(rgb_signal, fps=30):
    window_len = int(1.6 * fps)
    n = len(rgb_signal)
    if n < window_len:
        return chrom_algorithm(rgb_signal)

    P = np.array([[0, 1, -1], [-2, 1, 1]])
    bvp = np.zeros(n)

    for i in range(window_len, n):
        start = i - window_len
        window = rgb_signal[start:i].T
        Cn = window / (np.mean(window, axis=1, keepdims=True) + 1e-10)
        S = P @ Cn
        S1, S2 = S[0], S[1]
        alpha = np.std(S1) / (np.std(S2) + 1e-10)
        H = S1 - alpha * S2
        H = H - np.mean(H)
        bvp[start:i] += H

    bvp = (bvp - np.mean(bvp)) / (np.std(bvp) + 1e-10)
    return bvp


class RPPGExtractor:
    def __init__(self, fps=30, lowcut=0.7, highcut=4.0):
        self.fps = fps
        self.lowcut = lowcut
        self.highcut = highcut

    def extract(self, rgb_trace, return_signal=False):
        min_frames = max(30, int(self.fps * 0.3 * 5))
        if len(rgb_trace) < min_frames:
            empty = {"bpm": 0.0, "bpm_var": 0.0, "hrv_rmssd": 0.0, "hrv_sdnn": 0.0, "snr": 0.0, "skew": 0.0, "kurt": 0.0}
            if return_signal:
                return empty, np.array([]), np.array([])
            return empty

        bvp_chrom = chrom_algorithm(rgb_trace)
        bvp_pos = pos_algorithm(rgb_trace, self.fps)
        bvp = (bvp_chrom + bvp_pos) / 2.0

        hrv, filtered, peaks = compute_hrv(bvp, self.fps, self.lowcut, self.highcut, return_signal=True)
        hrv["skew"] = float(stats.skew(bvp))
        hrv["kurt"] = float(stats.kurtosis(bvp))

        if return_signal:
            return hrv, filtered, peaks
        return hrv
