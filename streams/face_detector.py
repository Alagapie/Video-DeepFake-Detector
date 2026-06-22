import cv2
import numpy as np


class FaceDetector:
    def __init__(self, confidence=0.5):
        self.confidence = confidence
        self.fd = None
        self._init_backend()

    def _init_backend(self):
        try:
            from mediapipe.python.solutions.face_detection import FaceDetection
            self.fd = FaceDetection(
                model_selection=1, min_detection_confidence=self.confidence
            )
        except Exception:
            self.fd = None

    def detect(self, frame):
        if self.fd is not None:
            return self._detect_mediapipe(frame)
        return self._detect_haar(frame)

    def _detect_mediapipe(self, frame):
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.fd.process(rgb)
            if results.detections:
                det = results.detections[0]
                h, w = frame.shape[:2]
                bbox = det.location_data.relative_bounding_box
                x = int(max(0, bbox.xmin * w))
                y = int(max(0, bbox.ymin * h))
                bw = int(min(bbox.width * w, w - x))
                bh = int(min(bbox.height * h, h - y))
                return (x, y, bw, bh)
        except Exception:
            pass
        return None

    def _detect_haar(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
        if len(faces) > 0:
            x, y, w, h = faces[0]
            return (x, y, w, h)
        return None

    def crop_face(self, frame, bbox, margin=0.2):
        x, y, w, h = bbox
        xm = int(w * margin)
        ym = int(h * margin)
        x1 = max(0, x - xm)
        y1 = max(0, y - ym)
        x2 = min(frame.shape[1], x + w + xm)
        y2 = min(frame.shape[0], y + h + ym)
        return frame[y1:y2, x1:x2]

    def get_roi_rgb(self, frame, bbox):
        x, y, w, h = bbox
        roi = frame[y:y + h, x:x + w]
        if roi.size == 0:
            return None
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([0, 15, 30]), np.array([20, 150, 255]))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        if np.sum(mask) == 0:
            mask[:] = 255
        mean = cv2.mean(roi, mask)[:3]
        return np.array([mean[2], mean[1], mean[0]], dtype=np.float32)

    def release(self):
        if self.fd is not None and hasattr(self.fd, 'close'):
            self.fd.close()
