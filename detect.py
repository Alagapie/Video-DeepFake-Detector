#!/usr/bin/env python3
import os
import sys
import yaml
import argparse
import json
import numpy as np

from utils.video_io import extract_frames
from streams.face_detector import FaceDetector
from streams.visual_stream import VisualStream
from streams.rppg_stream import RPPGExtractor
from fusion.build_features import build_feature_vector, FEATURE_NAMES
from fusion.decision import FusionEngine


def analyze_video(video_path, config):
    sample_rate = config["inference"]["frame_sample_rate"]
    max_frames = config["inference"]["max_frames"]
    target_size = config["inference"]["target_size"]
    face_conf = config["inference"]["face_confidence"]
    rppg_cfg = config["rppg"]

    frames, fps = extract_frames(video_path, sample_rate, max_frames, target_size)
    if not frames:
        print("ERROR: Could not read video.")
        sys.exit(1)

    print(f"  Frames extracted: {len(frames)}  (sampled at {sample_rate} fps)")

    fd = FaceDetector(confidence=face_conf)
    visual = VisualStream(config["weights_dir"])
    rppg = RPPGExtractor(fps=sample_rate, lowcut=rppg_cfg["bandpass_low"], highcut=rppg_cfg["bandpass_high"])
    fusion = FusionEngine(config)
    fusion.load_xgb()

    face_crops = []
    rgb_trace = []

    for frame in frames:
        bbox = fd.detect(frame)
        if bbox is not None:
            crop = fd.crop_face(frame, bbox)
            face_crops.append(crop)
            rgb = fd.get_roi_rgb(frame, bbox)
            if rgb is not None:
                rgb_trace.append(rgb)

    fd.release()

    if not face_crops:
        print("  WARNING: No face detected in any frame.")
        return {
            "video": os.path.basename(video_path),
            "decision": "NO_FACE",
            "confidence": 1.0,
            "prob_real": 0.5,
            "visual_score": 0.5,
            "temporal_std": 0.0,
            "per_model_scores": {"resnet18": 0.5, "vit_b16": 0.5},
            "rppg": {k: 0.0 for k in ["bpm", "bpm_var", "hrv_rmssd", "hrv_sdnn", "snr", "skew", "kurt"]},
            "features": {},
            "reason": "No face detected in any frame",
        }

    print(f"  Frames with face: {len(face_crops)}")

    visual_score, temporal_std, per_model = visual.predict(face_crops)

    rppg_trace = np.array(rgb_trace) if rgb_trace else np.zeros((len(face_crops), 3))
    rppg_features = rppg.extract(rppg_trace)

    features = build_feature_vector(visual_score, temporal_std, rppg_features)
    decision, confidence, prob_real, reason = fusion.predict(features)

    return {
        "video": os.path.basename(video_path),
        "decision": decision,
        "confidence": round(confidence, 4),
        "prob_real": round(prob_real, 4),
        "visual_score": round(visual_score, 4),
        "temporal_std": round(temporal_std, 4),
        "per_model_scores": {k: round(v, 4) for k, v in per_model.items()},
        "rppg": {k: round(v, 2) if isinstance(v, float) else v for k, v in rppg_features.items()},
        "features": {FEATURE_NAMES[i]: round(float(features[i]), 4) for i in range(len(FEATURE_NAMES))},
        "reason": reason,
    }


def print_report(result):
    print("\n" + "=" * 55)
    print("  DEEPFAKE DETECTOR — PRODUCTION v1.0")
    print("=" * 55)

    dec = result["decision"]
    if dec == "REAL":
        status = "✓ REAL"
    elif dec == "FAKE":
        status = "✗ FAKE"
    elif dec == "NO_FACE":
        status = "— NO FACE DETECTED"
    else:
        status = "? UNCERTAIN"

    print(f"  DECISION:     {status}")
    print(f"  Confidence:   {result['confidence']:.2%}")
    print(f"  Probability:  {result['prob_real']:.2%} real")
    print("-" * 55)

    print(f"  VISUAL STREAM")
    print(f"    Ensemble:   {result['visual_score']:.4f}")
    for name, score in result["per_model_scores"].items():
        print(f"    {name:12s}: {score:.4f}")
    print(f"    Temporal σ: {result['temporal_std']:.4f}")

    print(f"\n  rPPG STREAM")
    for k, v in result["rppg"].items():
        print(f"    {k:12s}: {v}")

    if result.get("reason"):
        print(f"\n  REASON: {result['reason']}")

    print(f"\n  FEATURES")
    for k, v in result["features"].items():
        print(f"    {k:15s}: {v:.4f}")

    print("=" * 55)


def main():
    parser = argparse.ArgumentParser(description="Deepfake Detector")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--max-frames", type=int, help="Override max frames")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: Video not found: {args.video}")
        sys.exit(1)

    with open(args.config) as f:
        config = yaml.safe_load(f)

    if args.max_frames:
        config["inference"]["max_frames"] = args.max_frames

    print(f"Analyzing: {args.video}")
    result = analyze_video(args.video, config)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
