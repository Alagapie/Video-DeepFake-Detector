import os
import uuid
import time
import io
import base64
import tempfile
import yaml
import numpy as np
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.video_io import extract_frames
from streams.face_detector import FaceDetector
from streams.visual_stream import VisualStream
from streams.rppg_stream import RPPGExtractor
from fusion.build_features import build_feature_vector, FEATURE_NAMES
from fusion.decision import FusionEngine
from report import generate_pdf

import cv2

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

_result_cache = {}
_CACHE_TTL = 600


def _clean_cache():
    now = time.time()
    stale = [k for k in list(_result_cache.keys()) if now - _result_cache[k][2] > _CACHE_TTL]
    for k in stale:
        del _result_cache[k]


app = FastAPI(title="Deepfake Detector API", version="3.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


def analyze_video_bytes(video_bytes: bytes, filename: str):
    sample_rate = config["inference"]["frame_sample_rate"]
    max_frames = config["inference"]["max_frames"]
    face_conf = config["inference"]["face_confidence"]
    rppg_cfg = config["rppg"]

    suffix = Path(filename).suffix or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    try:
        frames, fps = extract_frames(tmp_path, sample_rate, max_frames)
        if not frames:
            raise HTTPException(400, "Could not read video frames.")

        fd = FaceDetector(confidence=face_conf)
        visual = VisualStream(config["weights_dir"])
        rppg = RPPGExtractor(
            fps=sample_rate,
            lowcut=rppg_cfg["bandpass_low"],
            highcut=rppg_cfg["bandpass_high"],
        )
        fusion = FusionEngine(config)
        fusion.load_xgb()

        face_crops = []
        face_crops_raw = []
        rgb_trace = []
        for frame in frames:
            bbox = fd.detect(frame)
            if bbox is not None:
                crop = fd.crop_face(frame, bbox)
                face_crops.append(crop)
                if len(face_crops_raw) < 3:
                    ret, buf = cv2.imencode(".png", crop)
                    if ret:
                        face_crops_raw.append(base64.b64encode(buf).decode())
                rgb = fd.get_roi_rgb(frame, bbox)
                if rgb is not None:
                    rgb_trace.append(rgb)
        fd.release()

        if not face_crops:
            result = {
                "video": filename, "decision": "NO_FACE", "confidence": 1.0, "prob_real": 0.5,
                "visual_score": 0.5, "temporal_std": 0.0,
                "per_model_scores": {"resnet18": 0.5, "vit_b16": 0.5},
                "rppg": {k: 0.0 for k in ["bpm", "bpm_var", "hrv_rmssd", "hrv_sdnn", "snr", "skew", "kurt"]},
                "features": {}, "reason": "No face detected in any frame",
            }
            return result, None

        visual_score, temporal_std, per_model = visual.predict(face_crops)
        rppg_trace = np.array(rgb_trace) if rgb_trace else np.zeros((len(face_crops), 3))
        rppg_features, filtered_signal, peak_indices = rppg.extract(rppg_trace, return_signal=True)
        features = build_feature_vector(visual_score, temporal_std, rppg_features)
        decision, confidence, prob_real, reason = fusion.predict(features)

        result = {
            "video": filename, "decision": decision, "confidence": round(confidence, 4),
            "prob_real": round(prob_real, 4), "visual_score": round(visual_score, 4),
            "temporal_std": round(temporal_std, 4),
            "per_model_scores": {k: round(v, 4) for k, v in per_model.items()},
            "rppg": {k: round(v, 2) if isinstance(v, float) else v for k, v in rppg_features.items()},
            "features": {FEATURE_NAMES[i]: round(float(features[i]), 2) for i in range(len(FEATURE_NAMES))},
            "reason": reason,
        }

        xai_data = {
            "face_crops": face_crops_raw,
            "filtered_signal": filtered_signal.tolist() if len(filtered_signal) else [],
            "peaks": peak_indices.tolist() if len(peak_indices) else [],
        }
        return result, xai_data
    finally:
        os.unlink(tmp_path)


@app.get("/")
def root():
    return {"app": "Deepfake Detector", "version": "3.0.0", "status": "ready"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "No file provided.")
    video_bytes = await file.read()
    result, xai_data = analyze_video_bytes(video_bytes, file.filename)
    report_id = str(uuid.uuid4())[:8]
    _clean_cache()
    _result_cache[report_id] = (result, xai_data, time.time())
    return JSONResponse({**result, "report_id": report_id})


@app.get("/report/{report_id}")
async def report(report_id: str):
    entry = _result_cache.get(report_id)
    if entry is None:
        raise HTTPException(404, "Report not found or expired. Call POST /detect first.")
    result, xai_data, _ = entry
    pdf_bytes = generate_pdf(result, xai_data=xai_data)
    filename = Path(result["video"]).stem + "_forensic_report.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
