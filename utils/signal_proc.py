import numpy as np
from scipy.signal import butter, filtfilt, find_peaks


def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = max(lowcut / nyquist, 1e-6)
    high = min(highcut / nyquist, 0.999)
    b, a = butter(order, [low, high], btype='band')
    return b, a


def bandpass_filter(signal, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    axis = -1
    if signal.ndim == 1:
        signal = signal[np.newaxis, :]
        axis = -1
    filtered = filtfilt(b, a, signal, axis=axis)
    return filtered[0] if filtered.shape[0] == 1 else filtered


def compute_hrv(bvp_signal, fps, lowcut=0.7, highcut=4.0, return_signal=False):
    filtered = bandpass_filter(bvp_signal, lowcut, highcut, fps)

    peaks, properties = find_peaks(filtered, distance=max(int(fps * 0.3), 1), height=0)
    if len(peaks) < 2:
        result = {
            "bpm": 0.0,
            "bpm_var": 0.0,
            "hrv_rmssd": 0.0,
            "hrv_sdnn": 0.0,
            "snr": 0.0,
        }
        if return_signal:
            return result, filtered, peaks
        return result

    ibi = np.diff(peaks) / fps * 1000.0
    heart_rate = 60000.0 / np.mean(ibi)
    bpm_var = np.std(60000.0 / ibi) if len(ibi) > 1 else 0.0
    hrv_rmssd = np.sqrt(np.mean(np.diff(ibi) ** 2))
    hrv_sdnn = np.std(ibi)

    signal_power = np.var(filtered)
    noise = bvp_signal - filtered
    noise_power = np.var(noise) + 1e-10
    snr = 10.0 * np.log10(signal_power / noise_power)

    result = {
        "bpm": float(heart_rate),
        "bpm_var": float(bpm_var),
        "hrv_rmssd": float(hrv_rmssd),
        "hrv_sdnn": float(hrv_sdnn),
        "snr": float(snr),
    }
    if return_signal:
        return result, filtered, peaks
    return result
