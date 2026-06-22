import os
import json
import numpy as np

from fusion.build_features import FEATURE_NAMES


class FusionEngine:
    def __init__(self, config):
        self.real_threshold = config["fusion"]["real_threshold"]
        self.fake_threshold = config["fusion"]["fake_threshold"]
        self.pulse_override = config["fusion"].get("pulse_override", 0.85)

    def load_xgb(self):
        return False

    def predict(self, features):
        visual_score = float(features[0])
        temporal_std = float(features[1]) if len(features) > 1 else 0.0
        bpm = float(features[2]) if len(features) > 2 else 0.0
        rmssd = float(features[4]) if len(features) > 4 else 0.0
        sdnn = float(features[5]) if len(features) > 5 else 0.0
        snr_val = float(features[6]) if len(features) > 6 else 0.0
        kurt_val = float(features[8]) if len(features) > 8 else 0.0
        has_valid_pulse = 50 <= bpm <= 120 and snr_val > 0
        rppg_has_data = bpm > 0 or snr_val != 0

        if temporal_std < 0.001:
            reason = "Frozen face — temporal variance near zero"
            return "FAKE", 1.0, 0.0, reason

        if (abs(kurt_val) > 10 or kurt_val < 0.5) and (rmssd > 200 or sdnn > 200):
            reason = f"Abnormal rPPG morphology (kurt={kurt_val:.1f}, HRV)"
            return "FAKE", 1.0, 0.0, reason

        if snr_val < 0 and (rmssd > 150 or sdnn > 150):
            reason = f"Low SNR ({snr_val:.1f}) with inflated HRV"
            return "FAKE", 1.0, 0.0, reason

        if not rppg_has_data:
            prob_real = min(visual_score, 0.70)
            reason = "No rPPG data — capped at 0.70"
            decision, confidence = self._threshold(prob_real)
            return decision, confidence, prob_real, reason

        rppg_score = 1.0 - abs(bpm - 75.0) / 75.0 if bpm > 0 else 0.5
        rppg_score = max(0.0, min(1.0, rppg_score))

        if snr_val < -2.0:
            visual_weight = 0.3
            rppg_weight = 0.7
            reason = "Low SNR — swapped to rPPG-heavy weights"
        else:
            visual_weight = 0.6
            rppg_weight = 0.4
            reason = "Standard weighted fusion"

        prob_real = float(visual_weight * visual_score + rppg_weight * rppg_score)

        if has_valid_pulse:
            prob_real = max(prob_real, self.pulse_override)
            reason = f"{reason}; valid pulse override → min {self.pulse_override}"

        decision, confidence = self._threshold(prob_real)
        return decision, confidence, prob_real, reason

    def _threshold(self, prob_real):
        if prob_real >= self.real_threshold:
            return "REAL", prob_real
        elif prob_real <= self.fake_threshold:
            return "FAKE", 1.0 - prob_real
        else:
            return "UNCERTAIN", max(prob_real, 1.0 - prob_real)
