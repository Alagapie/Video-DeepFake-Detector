import numpy as np

FEATURE_NAMES = [
    "visual_score",
    "temporal_std",
    "bpm",
    "bpm_var",
    "hrv_rmssd",
    "hrv_sdnn",
    "snr",
    "skew",
    "kurt",
]


def build_feature_vector(visual_score, temporal_std, rppg_features):
    features = np.zeros(len(FEATURE_NAMES), dtype=np.float32)
    features[0] = visual_score
    features[1] = temporal_std
    features[2] = rppg_features.get("bpm", 0.0)
    features[3] = rppg_features.get("bpm_var", 0.0)
    features[4] = rppg_features.get("hrv_rmssd", 0.0)
    features[5] = rppg_features.get("hrv_sdnn", 0.0)
    features[6] = rppg_features.get("snr", 0.0)
    features[7] = rppg_features.get("skew", 0.0)
    features[8] = rppg_features.get("kurt", 0.0)
    return features


def feature_dict_to_array(fd):
    return np.array([fd.get(n, 0.0) for n in FEATURE_NAMES], dtype=np.float32)
