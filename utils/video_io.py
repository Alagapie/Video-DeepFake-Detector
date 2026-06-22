import cv2
import numpy as np
from pathlib import Path


def extract_frames(video_path, sample_rate=1, max_frames=30, target_size=224):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        fps = 30

    frame_interval = int(fps / sample_rate) if sample_rate <= fps else 1

    frames = []
    frame_idx = 0
    while len(frames) < max_frames:
        ret = cap.grab()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            ret, frame = cap.retrieve()
            if not ret:
                break
            frames.append(frame)
        frame_idx += 1

    cap.release()
    return frames, fps


def preprocess_face(face_crop, target_size=224):
    h, w = face_crop.shape[:2]
    scale = target_size / max(h, w)
    if scale != 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        face_crop = cv2.resize(face_crop, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    y_off = (target_size - face_crop.shape[0]) // 2
    x_off = (target_size - face_crop.shape[1]) // 2
    canvas[y_off:y_off + face_crop.shape[0], x_off:x_off + face_crop.shape[1]] = face_crop

    rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB).astype(np.float32)
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    rgb = ((rgb / 255.0 - mean) / std).astype(np.float32)

    return np.transpose(rgb, (2, 0, 1))
