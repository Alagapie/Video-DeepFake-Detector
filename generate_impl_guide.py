import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


def create_impl_guide(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    pw = A4[0] - 40 * mm

    styles.add(ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=26, leading=32,
                               alignment=TA_CENTER, spaceAfter=8, textColor=HexColor('#1a365d')))
    styles.add(ParagraphStyle('CSub', fontName='Helvetica', fontSize=14, leading=18,
                               alignment=TA_CENTER, spaceAfter=4, textColor=HexColor('#4a5568')))
    styles.add(ParagraphStyle('STitle', fontName='Helvetica-Bold', fontSize=18, leading=22,
                               spaceBefore=28, spaceAfter=12, textColor=HexColor('#1a365d')))
    styles.add(ParagraphStyle('SubT', fontName='Helvetica-Bold', fontSize=13, leading=16,
                               spaceBefore=16, spaceAfter=6, textColor=HexColor('#2d3748')))
    styles.add(ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14,
                               spaceAfter=6, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle('Bul', fontName='Helvetica', fontSize=10, leading=14,
                               spaceAfter=3, leftIndent=20, bulletIndent=8))
    styles.add(ParagraphStyle('CodeBlock', fontName='Courier', fontSize=7.5, leading=10,
                               leftIndent=12, spaceAfter=8,
                               backColor=HexColor('#f7fafc'),
                               borderWidth=1, borderColor=HexColor('#e2e8f0'),
                               borderPadding=8))
    styles.add(ParagraphStyle('TC', fontName='Helvetica', fontSize=8.5, leading=11, alignment=TA_LEFT))
    styles.add(ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
                               alignment=TA_CENTER, textColor=white))
    styles.add(ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=9, leading=12,
                               spaceAfter=6, leftIndent=12, textColor=HexColor('#718096')))
    styles.add(ParagraphStyle('Footer', fontName='Helvetica', fontSize=7, leading=9,
                               textColor=HexColor('#a0aec0'), alignment=TA_CENTER))

    story = []

    def add_table(headers, rows, col_widths):
        data = [[Paragraph(h, styles['TH']) for h in headers]]
        for row in rows:
            data.append([Paragraph(str(c), styles['TC']) for c in row])
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ]))
        return t

    # ========= COVER =========
    story.append(Spacer(1, 80))
    story.append(Paragraph("DeepGuard", styles['CTitle']))
    story.append(Paragraph("Technical Architecture & Implementation Guide", styles['CSub']))
    story.append(Spacer(1, 12))
    story.append(Table([[""]], colWidths=[pw], style=TableStyle([
        ('LINEBELOW', (0, 0), (0, 0), 2, HexColor('#2b6cb0'))
    ])))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Version 3.0.0 | June 2026", styles['CSub']))
    story.append(Spacer(1, 60))
    story.append(PageBreak())

    # ========= TOC =========
    story.append(Paragraph("Table of Contents", styles['STitle']))
    toc = [
        "1. System Overview",
        "2. Architecture Diagram & Component Breakdown",
        "3. Video Pipeline (Input \u2192 Face Detection \u2192 Frame Processing)",
        "4. Visual Stream (ResNet-18 + ViT-B/16)",
        "5. rPPG Stream (CHROM + POS)",
        "6. Feature Vector Construction",
        "7. Fusion Engine & Decision Rules",
        "8. Decision Flowchart",
        "9. API Layer (FastAPI Server)",
        "10. PDF Report Generation",
        "11. CI/CD & Deployment Pipeline",
        "12. Configuration Reference (config.yaml)",
        "13. File-by-File Code Map",
        "14. Dependency Graph",
    ]
    for i, t in enumerate(toc, 1):
        story.append(Paragraph(f"<b>{t}</b>", styles['Body']))
    story.append(PageBreak())

    # ========= 1. SYSTEM OVERVIEW =========
    story.append(Paragraph("1. System Overview", styles['STitle']))
    story.append(Paragraph(
        "DeepGuard is a production-ready video deepfake detection system that analyzes videos "
        "using two independent biological signals and combines them through a deterministic "
        "rule-based fusion engine. The system requires no GPU for inference, no ML training "
        "for the fusion layer, and is deployed serverlessly on Azure Container Apps.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    overview_data = [
        ["<b>Aspect</b>", "<b>Detail</b>"],
        ["Detection approach", "Dual-stream: visual (ResNet-18 + ViT-B/16) + physiological rPPG (CHROM + POS)"],
        ["Fusion method", "Weighted score (0.6 visual + 0.4 rPPG) with 5 deterministic override rules"],
        ["Inference hardware", "CPU only (Intel/AMD x86_64, no GPU required)"],
        ["Pretrained models", "ResNet-18 + ViT-B/16 from HuggingFace (abraraltaf92/deepfake-detection-models)"],
        ["Face detection", "OpenCV Haar Cascade (primary), MediaPipe (fallback)"],
        ["Output types", "JSON verdict + downloadable PDF forensic report"],
        ["Deployment", "Docker \u2192 Azure Container Registry \u2192 Azure Container Apps"],
        ["Language", "Python 3.10"],
        ["Docker base", "python:3.10-slim-bookworm (Debian 12)"],
    ]
    story.append(add_table(overview_data[0], overview_data[1:], [120, pw - 120]))
    story.append(PageBreak())

    # ========= 2. ARCHITECTURE DIAGRAM =========
    story.append(Paragraph("2. Architecture Diagram", styles['STitle']))
    story.append(Paragraph(
        "The diagram below shows the complete data flow from video upload to final verdict and PDF report. "
        "Two parallel streams process visual and physiological signals independently before converging "
        "at the fusion engine.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))
    if os.path.exists('architecture_diagram.png'):
        story.append(Image('architecture_diagram.png', width=pw, height=pw * 0.72))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Component Breakdown", styles['SubT']))
    comps_data = [
        ["<b>Component</b>", "<b>File(s)</b>", "<b>Responsibility</b>"],
        ["Video Input & Frame Extraction", "utils/video_io.py", "Reads video, extracts frames at configurable sample rate (default 3 fps), limits to max_frames (default 90)"],
        ["Face Detector", "streams/face_detector.py", "Detects faces via OpenCV Haar cascade; extracts face crops and skin-masked ROIs for rPPG"],
        ["Visual Stream", "streams/visual_stream.py", "Two models (ResNet-18 + ViT-B/16) classify each face crop; returns per-model probability + temporal variance"],
        ["rPPG Stream", "streams/rppg_stream.py", "Extracts pulse signal from ROI RGB trace using CHROM and POS algorithms; computes BPM, HRV, SNR, kurtosis"],
        ["Feature Builder", "fusion/build_features.py", "Assembles 9-dimensional feature vector from visual + rPPG outputs"],
        ["Fusion Engine", "fusion/decision.py", "Weighted fusion + 5 override rules; returns decision, confidence, prob_real, reason string"],
        ["API Server", "api.py", "FastAPI server: POST /detect, GET /report/{id}, GET /. CORS middleware, in-memory result cache (10 min TTL)"],
        ["PDF Report", "report.py", "ReportLab-based PDF generator with decision badge, metric tables, rPPG waveform chart, face crops, glossary"],
        ["Config", "config.yaml", "Central configuration: frame rate, thresholds, weights path, rPPG bandpass params"],
    ]
    story.append(add_table(comps_data[0], comps_data[1:], [80, 100, pw - 180]))
    story.append(PageBreak())

    # ========= 3. VIDEO PIPELINE =========
    story.append(Paragraph("3. Video Pipeline: Input \u2192 Face Detection \u2192 Frame Processing", styles['STitle']))
    story.append(Paragraph("3.1 Frame Extraction (utils/video_io.py)", styles['SubT']))
    story.append(Paragraph(
        "The pipeline begins in <font face='Courier'>analyze_video_bytes()</font> in <font face='Courier'>api.py</font>. "
        "The uploaded video bytes are written to a temporary file, then <font face='Courier'>extract_frames()</font> "
        "reads the video using OpenCV's <font face='Courier'>VideoCapture</font>.",
        styles['Body']
    ))

    frame_code = '''def extract_frames(video_path, sample_rate=3, max_frames=90):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(fps / sample_rate))
    frames = []
    frame_idx = 0
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_idx += 1
    cap.release()
    return frames, fps'''
    story.append(Preformatted(frame_code, styles['CodeBlock']))
    story.append(Paragraph(
        "<b>Parameters:</b> <font face='Courier'>sample_rate=3</font> (3 fps) balances rPPG viability (Nyquist ~90 BPM) "
        "with CPU inference speed. <font face='Courier'>max_frames=90</font> limits to 30 seconds of video.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Face Detection (streams/face_detector.py)", styles['SubT']))
    story.append(Paragraph(
        "The <font face='Courier'>FaceDetector</font> class wraps OpenCV's Haar cascade classifier "
        "(<font face='Courier'>haarcascade_frontalface_default.xml</font>). Each frame is processed: "
        "the largest face bounding box is selected (highest confidence). If Haar fails to detect any face "
        "but skin pixels are present, MediaPipe falls back.",
        styles['Body']
    ))

    fd_code = '''class FaceDetector:
    def __init__(self, confidence=0.5):
        self.haar = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.mediapipe = mp.solutions.face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=confidence
        )

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.haar.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            return (x, y, w, h)
        return None  # fallback to MediaPipe if needed

    def crop_face(self, frame, bbox):
        x, y, w, h = bbox
        margin = int(0.2 * w)
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(frame.shape[1], x + w + margin)
        y2 = min(frame.shape[0], y + h + margin)
        return frame[y1:y2, x1:x2]

    def get_roi_rgb(self, frame, bbox):
        \"\"\"Extract skin-masked ROI for rPPG.\"\"\"
        x, y, w, h = bbox
        roi = frame[y:y+h, x:x+w]
        hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        lower = np.array([0, 20, 50])
        upper = np.array([20, 150, 255])
        mask = cv2.inRange(hsv, lower, upper)
        if np.sum(mask) == 0:
            return roi.mean(axis=(0, 1))  # fallback to mean RGB
        return cv2.mean(roi, mask=mask)[:3]'''
    story.append(Preformatted(fd_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Per-Frame Processing Loop", styles['SubT']))
    story.append(Paragraph(
        "For each extracted frame, the pipeline:\n"
        "(1) Detects face via <font face='Courier'>FaceDetector.detect()</font>\n"
        "(2) Crops face region via <font face='Courier'>FaceDetector.crop_face()</font>\n"
        "(3) Collects first 3 crops as base64 PNG for PDF face thumbnails\n"
        "(4) Extracts skin-masked ROI RGB via <font face='Courier'>FaceDetector.get_roi_rgb()</font>\n\n"
        "If <b>no face is detected in any frame</b>, the pipeline short-circuits and returns "
        "NO_FACE immediately.",
        styles['Body']
    ))
    story.append(PageBreak())

    # ========= 4. VISUAL STREAM =========
    story.append(Paragraph("4. Visual Stream: ResNet-18 + ViT-B/16", styles['STitle']))
    story.append(Paragraph(
        "The visual stream uses two pretrained convolutional/transformer models loaded from HuggingFace. "
        "Both models were pretrained on Celeb-DF v2 by <font face='Courier'>abraraltaf92</font> and "
        "are used <b>without any fine-tuning</b>. They run on CPU with forced <font face='Courier'>device='cpu'</font>.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.1 Model Architecture (streams/visual_stream.py)", styles['SubT']))

    vis_code = '''class ResNetVideoClassifier:
    \"\"\"ResNet-18 backbone + custom head matching HF state dict.\"\"\"
    def __init__(self, weights_path):
        self.model = torch.load(weights_path, map_location='cpu')
        self.model.eval()

    def predict(self, face_crops):
        \"\"\"Returns (probability_deepfake, 0-1)\"\"\"
        tensor = preprocess_face(face_crops)  # [B, 3, 224, 224]
        with torch.no_grad():
            logits = self.model(tensor)
        probs = torch.softmax(logits, dim=1)[:, 1]
        return probs.mean().item()


class ViTVideoClassifier:
    \"\"\"ViT-B/16 backbone + custom head.\"\"\"
    def __init__(self, weights_path):
        self.model = torch.load(weights_path, map_location='cpu')
        self.model.eval()

    def predict(self, face_crops):
        tensor = preprocess_face(face_crops)
        with torch.no_grad():
            logits = self.model(tensor)
        probs = torch.softmax(logits, dim=1)[:, 1]
        return probs.mean().item()'''
    story.append(Preformatted(vis_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 Preprocessing Pipeline", styles['SubT']))
    pp_code = '''def preprocess_face(face_crops):
    \"\"\"ImageNet normalization, resize to 224x224.\"\"\"
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
    ])
    tensors = []
    for crop in face_crops:
        tensors.append(transform(crop.astype(np.float32)))
    return torch.stack(tensors)'''
    story.append(Preformatted(pp_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.3 Visual Score Computation", styles['SubT']))
    story.append(Paragraph(
        "The <font face='Courier'>VisualStream</font> class runs both models on all face crops and returns:",
        styles['Body']
    ))
    items = [
        "<b>per_model_scores:</b> {'resnet18': 0.85, 'vit_b16': 0.92} \u2014 individual model probabilities (deepfake=1.0)",
        "<b>visual_score:</b> average of both model scores (used as the combined visual signal)",
        "<b>temporal_std:</b> standard deviation of pixel values across consecutive crops. "
        "A value near 0.001 indicates a frozen face (no natural movement) \u2014 an immediate FAKE signal.",
    ]
    for item in items:
        story.append(Paragraph(f"\u2022 {item}", styles['Bul']))
    story.append(PageBreak())

    # ========= 5. rPPG STREAM =========
    story.append(Paragraph("5. rPPG Stream: CHROM + POS", styles['STitle']))
    story.append(Paragraph(
        "Remote Photoplethysmography (rPPG) extracts the subtle color changes in facial skin caused by "
        "blood volume pulses. The system uses two classical algorithms from the NeuroKit2 library: "
        "<b>CHROM</b> (chrominance-based) and <b>POS</b> (Plane Orthogonal to Skin). Both are well-established "
        "in the biomedical signal processing literature and require no GPU.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.1 Signal Processing Pipeline (streams/rppg_stream.py)", styles['SubT']))
    rppg_code = '''class RPPGExtractor:
    def __init__(self, fps=3, lowcut=0.8, highcut=3.0):
        self.fps = fps
        self.lowcut = lowcut
        self.highcut = highcut

    def extract(self, rgb_trace, return_signal=False):
        # 1. Build BVP signal from RGB trace using CHROM/POS
        #    NeuroKit2: nk.ppg() or custom CHROM implementation
        bvp = self._chrom_alg(rgb_trace)

        # 2. Bandpass filter (Butterworth, 4th order)
        #    Clamps Wn to valid range [1e-6, 0.999] for low FPS
        sos = butter(4, [low, high], btype='band', fs=fps, output='sos')
        filtered = sosfiltfilt(sos, bvp)

        # 3. Peak detection (SciPy find_peaks)
        #    Minimum distance = fps * 0.5 (catches BPM up to 120)
        distance = max(1, int(fps * 0.5))
        peaks, _ = find_peaks(filtered, distance=distance)

        # 4. Compute metrics
        bpm = len(peaks) / (len(bvp) / fps) * 60 if len(bvp) > 0 else 0
        hrv_rmssd = compute_rmssd(peaks) if len(peaks) > 1 else 0
        hrv_sdnn = compute_sdnn(peaks) if len(peaks) > 1 else 0
        snr = compute_snr(filtered, peaks)
        kurt = kurtosis(filtered)
        skew = skewness(filtered)

        features = {
            'bpm': bpm, 'bpm_var': bpm_var,
            'hrv_rmssd': hrv_rmssd, 'hrv_sdnn': hrv_sdnn,
            'snr': snr, 'skew': skew, 'kurt': kurt,
        }
        if return_signal:
            return features, filtered, peaks
        return features'''
    story.append(Preformatted(rppg_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.2 CHROM Algorithm (Simplified)", styles['SubT']))
    chrom_code = '''def _chrom_alg(self, rgb_trace):
    \"\"\"CHROM: Chrominance-based rPPG (de Haan & Jeanne 2009).\"\"\"
    # Normalize RGB channels
    r, g, b = rgb_trace[:, 0], rgb_trace[:, 1], rgb_trace[:, 2]
    Xs = 3 * r - 2 * g  # Red-green difference
    Ys = 1.5 * r + g - 1.5 * b  # Skin-tone compensated signal
    # Bandpass filter
    std_x = np.std(Xs); std_y = np.std(Ys)
    alpha = std_x / std_y if std_y > 0 else 1
    bvp = Xs - alpha * Ys
    return bvp'''
    story.append(Preformatted(chrom_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.3 Key Design Considerations", styles['SubT']))
    items = [
        "<b>Low FPS operation (3 Hz):</b> The Nyquist limit is 1.5 Hz (90 BPM). This is adequate for resting "
        "heart rate detection (50-80 BPM) but cannot detect tachycardia above 90 BPM.",
        "<b>Wn clamping:</b> At 3 fps, the bandpass range 0.8-3.0 Hz translates to normalized frequencies "
        "that may exceed Nyquist. The code clamps Wn to [1e-6, 0.999] to prevent filtfilt crashes.",
        "<b>Minimum frames:</b> At least 30 frames are required for reliable peak detection. "
        "The minimum is computed as <font face='Courier'>max(30, fps * 10)</font> which is 30 at 3 fps.",
        "<b>Peak distance floor:</b> <font face='Courier'>max(1, int(fps * 0.5))</font> prevents "
        "find_peaks from crashing at very low frame rates.",
        "<b>Skin mask fallback:</b> If no skin pixels are detected in the ROI (unlikely for face region), "
        "the mean RGB of the entire ROI is used instead.",
    ]
    for item in items:
        story.append(Paragraph(f"\u2022 {item}", styles['Bul']))
    story.append(PageBreak())

    # ========= 6. FEATURE VECTOR =========
    story.append(Paragraph("6. Feature Vector Construction (fusion/build_features.py)", styles['STitle']))
    story.append(Paragraph(
        "The fusion engine receives a 9-dimensional feature vector assembled from the visual and rPPG streams. "
        "Each feature is normalized to a 0-1 range using the <font face='Courier'>MinMaxScaler</font> from scikit-learn.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    fv_data = [
        ["<b>Index</b>", "<b>Feature</b>", "<b>Source</b>", "<b>Description</b>", "<b>Normalized Range</b>"],
        ["0", "visual_score", "Visual", "Combined ResNet-18 + ViT-B/16 probability", "0 (real) \u2192 1 (deepfake)"],
        ["1", "temporal_std", "Visual", "Frame-to-frame pixel variance", "0 (frozen) \u2192 1 (high motion)"],
        ["2", "bpm", "rPPG", "Heart rate (beats per minute)", "0 (no pulse) \u2192 1 (200 BPM)"],
        ["3", "bpm_var", "rPPG", "Heart rate variance across windows", "0 \u2192 1"],
        ["4", "hrv_rmssd", "rPPG", "Root Mean Square of Successive Differences", "0 \u2192 1 (normalized)"],
        ["5", "hrv_sdnn", "rPPG", "Standard Deviation of NN Intervals", "0 \u2192 1 (normalized)"],
        ["6", "snr", "rPPG", "Signal-to-noise ratio of rPPG signal", "0 (low SNR) \u2192 1 (high SNR)"],
        ["7", "skew", "rPPG", "Skewness of pulse waveform distribution", "0 \u2192 1"],
        ["8", "kurt", "rPPG", "Kurtosis of pulse waveform distribution", "0 \u2192 1"],
    ]
    story.append(add_table(fv_data[0], fv_data[1:], [35, 75, 50, pw - 160, 80]))
    story.append(Spacer(1, 8))

    fv_code = '''FEATURE_NAMES = ['visual_score', 'temporal_std', 'bpm', 'bpm_var',
                    'hrv_rmssd', 'hrv_sdnn', 'snr', 'skew', 'kurt']

def build_feature_vector(visual_score, temporal_std, rppg_dict):
    raw = np.array([
        visual_score, temporal_std,
        rppg_dict['bpm'], rppg_dict['bpm_var'],
        rppg_dict['hrv_rmssd'], rppg_dict['hrv_sdnn'],
        rppg_dict['snr'], rppg_dict['skew'], rppg_dict['kurt'],
    ])
    # MinMaxScaler fitted on precomputed min/max from ASVspoof
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(np.array([FEATURE_MIN, FEATURE_MAX]).T)
    return scaler.transform(raw.reshape(1, -1)).flatten()'''
    story.append(Preformatted(fv_code, styles['CodeBlock']))
    story.append(PageBreak())

    # ========= 7. FUSION ENGINE =========
    story.append(Paragraph("7. Fusion Engine & Decision Rules (fusion/decision.py)", styles['STitle']))
    story.append(Paragraph(
        "The <font face='Courier'>FusionEngine</font> is the core decision-making component. It takes the "
        "9-dimensional feature vector and applies a weighted fusion formula followed by 5 deterministic "
        "physiological override rules. Each rule returns a <b>decision</b>, <b>confidence</b>, "
        "<b>prob_real</b>, and a human-readable <b>reason</b> string.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    fusion_code = '''class FusionEngine:
    def __init__(self, config):
        self.real_thresh = config['inference']['real_threshold']     # 0.85
        self.fake_thresh = config['inference']['fake_threshold']     # 0.25
        self.pulse_override = config['inference']['pulse_override']  # 0.85

    def predict(self, features):
        # Extract individual features
        visual_score = features[0]
        temporal_std = features[1]
        bpm = features[2]
        hrv_rmssd = features[4]
        hrv_sdnn = features[5]
        snr = features[6]
        kurt = features[8]

        # ---- RULE 1: Frozen face ----
        if temporal_std < 0.001:
            return ('FAKE', 1.0, 0.0,
                    'Frozen face \\u2014 temporal variance near zero')

        # ---- RULE 2: Abnormal rPPG morphology ----
        if (kurt > 10 or kurt < 0.5) and (hrv_rmssd > 200 or hrv_sdnn > 200):
            return ('FAKE', 1.0, 0.0,
                    'Abnormal rPPG morphology \\u2014 spikey or flat pulse')

        # ---- RULE 3: Low SNR + inflated HRV ----
        if snr < -2.0 and (hrv_rmssd > 200 or hrv_sdnn > 200):
            return ('FAKE', 1.0, 0.0,
                    'Low rPPG signal quality \\u2014 noise masquerading as pulse')

        # ---- RULE 4: No rPPG data -> cap at 0.70 ----
        prob_real = 1.0 - (0.6 * visual_score + 0.4 * ...)
        if bpm == 0 and hrv_rmssd == 0:
            prob_real = min(prob_real, 0.70)
            return self._threshold(prob_real,
                'No physiological confirmation \\u2014 insufficient evidence')

        # ---- RULE 5: Normal weighted fusion ----
        prob_real = 1.0 - (0.6 * visual_score + 0.4 * ...)

        # Pulse override: valid pulse -> minimum 0.85
        if 50 <= bpm <= 120 and snr > 0:
            prob_real = max(prob_real, self.pulse_override)

        return self._threshold(prob_real, 'Standard weighted fusion')'''
    story.append(Preformatted(fusion_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.1 Priority Order (Strict)", styles['SubT']))
    priority_data = [
        ["<b>Priority</b>", "<b>Rule</b>", "<b>Condition</b>", "<b>Trigger</b>"],
        ["1", "Frozen face", "temporal_std < 0.001", "Physically impossible for real video"],
        ["2", "Abnormal morphology", "kurt > 10 or kurt < 0.5 + HRV > 200", "Deepfake pulse is spikey or flat noise"],
        ["3", "Low SNR + HRV", "SNR < -2.0 + HRV > 200", "Noise masquerading as pulse signal"],
        ["4", "No rPPG data", "bpm == 0 and hrv_rmssd == 0", "Cap prob_real at 0.70"],
        ["5", "Normal fusion", "Default path", "0.6 visual + 0.4 rPPG"],
        ["5a", "Pulse override", "50 <= bpm <= 120 and SNR > 0", "Valid pulse -> min 0.85 prob_real"],
    ]
    story.append(add_table(priority_data[0], priority_data[1:], [50, 95, 140, pw - 285]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Important:</b> Rules 1-3 return immediately and <b>do not</b> enter the normal fusion path. "
        "The pulse override (rule 5a) <b>only</b> applies within the normal fusion path, ensuring "
        "deterministic FAKE decisions cannot be overridden by a false-positive pulse detection.",
        styles['Note']
    ))
    story.append(PageBreak())

    # ========= 8. DECISION FLOWCHART =========
    story.append(Paragraph("8. Decision Flowchart", styles['STitle']))
    story.append(Paragraph(
        "The diagram below illustrates the decision engine's priority-ordered rules. Each diamond "
        "represents a deterministic check; if the condition matches, the system exits immediately "
        "with the corresponding verdict.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))
    if os.path.exists('decision_flowchart.png'):
        story.append(Image('decision_flowchart.png', width=pw, height=pw * 1.0))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Threshold Configuration", styles['SubT']))
    thresh_data = [
        ["<b>Parameter</b>", "<b>Value</b>", "<b>Effect</b>"],
        ["real_threshold", "0.85", "prob_real >= 0.85 -> REAL"],
        ["fake_threshold", "0.25", "prob_real <= 0.25 -> FAKE"],
        ["pulse_override", "0.85", "Valid pulse -> minimum prob_real = 0.85"],
        ["frame_sample_rate", "3", "Frames per second extracted from video"],
        ["max_frames", "90", "Maximum frames to process (30s at 3 fps)"],
    ]
    story.append(add_table(thresh_data[0], thresh_data[1:], [120, 60, pw - 180]))
    story.append(PageBreak())

    # ========= 9. API LAYER =========
    story.append(Paragraph("9. API Layer (FastAPI Server)", styles['STitle']))
    story.append(Paragraph(
        "The API is built with FastAPI and runs on Uvicorn. It exposes three endpoints and manages "
        "an in-memory result cache with a 10-minute TTL.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    api_code = '''app = FastAPI(title="Deepfake Detector API", version="3.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# In-memory cache: {report_id: (result_dict, xai_dict, timestamp)}
_result_cache = {}
_CACHE_TTL = 600  # 10 minutes

@app.get("/")
def root():
    return {"app": "Deepfake Detector", "version": "3.0.0", "status": "ready"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
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
        raise HTTPException(404, "Report not found or expired.")
    result, xai_data, _ = entry
    pdf_bytes = generate_pdf(result, xai_data=xai_data)
    return Response(content=pdf_bytes, media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=..."})'''
    story.append(Preformatted(api_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("9.1 Cache Design", styles['SubT']))
    cache_items = [
        "<b>Structure:</b> Dictionary keyed by 8-character hex <font face='Courier'>report_id</font>",
        "<b>Value:</b> Tuple of <font face='Courier'>(result: dict, xai_data: dict, timestamp: float)</font>",
        "<b>Eviction:</b> Cleaned on every <font face='Courier'>POST /detect</font> call (lazy expiry)",
        "<b>TTL:</b> 600 seconds (10 minutes). After expiry, <font face='Courier'>GET /report/{id}</font> returns 404",
    ]
    for item in cache_items:
        story.append(Paragraph(f"\u2022 {item}", styles['Bul']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("9.2 CORS Configuration", styles['SubT']))
    story.append(Paragraph(
        "CORS is wide open for development: <font face='Courier'>allow_origins=[\"*\"]</font>, "
        "<font face='Courier'>allow_methods=[\"*\"]</font>, <font face='Courier'>allow_headers=[\"*\"]</font>. "
        "The <font face='Courier'>Content-Disposition</font> header is exposed to allow the browser to "
        "detect the PDF download filename. Credentialed requests are not supported; "
        "if needed, replace <font face='Courier'>[\"*\"]</font> with specific origins.",
        styles['Body']
    ))
    story.append(PageBreak())

    # ========= 10. PDF REPORT =========
    story.append(Paragraph("10. PDF Report Generation (report.py)", styles['STitle']))
    story.append(Paragraph(
        "The PDF report is generated using <b>ReportLab</b>, a professional-grade PDF library. "
        "The <font face='Courier'>generate_pdf(result, xai_data=None)</font> function produces a "
        "multi-section forensic report as a bytes object ready for HTTP response.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    report_items = [
        "<b>Decision Badge:</b> A colored box at the top showing REAL (green), FAKE (red), "
        "UNCERTAIN (amber), or NO_FACE (gray), rendered using ReportLab's Paragraph with HTML styling",
        "<b>Video Info Section:</b> Filename, duration estimate, frame count",
        "<b>Visual Stream Table:</b> ResNet-18 score, ViT-B/16 score, temporal variance, "
        "with reference baselines in gray text and color-coded health indicators "
        "(green = normal, yellow = borderline, red = suspicious)",
        "<b>rPPG Metrics Table:</b> BPM, HRV (RMSSD), HRV (SDNN), SNR, skewness, kurtosis. "
        "Each metric has a color-coded assessment in the Status column",
        "<b>rPPG Waveform Chart:</b> A matplotlib-generated PNG showing the filtered BVP signal "
        "with detected pulse peaks marked as red dots, embedded in the PDF",
        "<b>Fusion Features Table:</b> All 9 normalized features displayed with color highlights "
        "(red for suspicious values, yellow for borderline)",
        "<b>Face Crop Thumbnails:</b> Up to 3 sample face crops from the video (early, middle, late frames), "
        "encoded as base64 PNG and embedded in the PDF",
        "<b>Pipeline Metadata Footer:</b> Model versions, feature normalization info, inference timestamp",
        "<b>Metrics Reference Glossary:</b> Plain-English explanations of every metric in the report, "
        "making the report accessible to non-technical stakeholders (law enforcement, journalists, compliance teams)",
    ]
    for item in report_items:
        story.append(Paragraph(f"\u2022 {item}", styles['Bul']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Report Generation Flow:", styles['SubT']))
    report_code = '''def generate_pdf(result, xai_data=None):
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    # 1. Decision badge (color-coded Paragraph)
    # 2. Video info table
    # 3. Visual stream metrics table
    # 4. rPPG metrics table with health assessments
    # 5. rPPG waveform chart (matplotlib -> BytesIO -> Image)
    # 6. Face crop thumbnails
    # 7. Fusion features table
    # 8. Metadata footer
    # 9. Metrics reference glossary (appendix)
    doc.build(story)
    return buffer.getvalue()'''
    story.append(Preformatted(report_code, styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "The report generation is <b>entirely server-side</b>. No external API or template engine "
        "is used. The report is generated on-the-fly and returned as a byte stream.",
        styles['Body']
    ))
    story.append(PageBreak())

    # ========= 11. CI/CD & DEPLOYMENT =========
    story.append(Paragraph("11. CI/CD & Deployment Pipeline", styles['STitle']))
    story.append(Paragraph(
        "The system is deployed on Azure Container Apps using a multi-stage Docker build "
        "pipeline. The deployment is triggered manually via Azure CLI commands.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))

    if os.path.exists('deployment_pipeline.png'):
        story.append(Image('deployment_pipeline.png', width=pw, height=pw * 0.38))
    story.append(Spacer(1, 8))

    story.append(Paragraph("11.1 Docker Build (Dockerfile)", styles['SubT']))
    docker_code = '''# Stage 1: Builder
FROM python:3.10-slim-bookworm AS builder

# Install OpenCV dependencies (Debian 12 bookworm)
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender1

WORKDIR /app
COPY requirements.txt .

# CPU-only PyTorch (install FIRST to avoid --index-url override)
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \\
    torch torchvision

# Remaining packages from PyPI
RUN pip install --no-cache-dir -r requirements.txt

# Download pretrained models at build time
COPY download_models.py .
RUN python download_models.py

# Stage 2: Runtime
FROM python:3.10-slim-bookworm
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app
COPY . /app
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]'''
    story.append(Preformatted(docker_code, styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("11.2 Deployment Commands", styles['SubT']))
    deploy_code = '''# 1. Build from GitHub source
az acr build --registry deepfakeprojectacr2026 \\
  --image video-deepfake-detector:latest \\
  https://github.com/Alagapie/Video-DeepFake-Detector.git

# 2. Create Container Apps environment (one-time)
az containerapp env create --name detector-env \\
  --resource-group audio-deepfake-rg --location francecentral

# 3. Deploy the app
az containerapp create --name deepfake-api \\
  --resource-group audio-deepfake-rg \\
  --environment detector-env \\
  --image deepfakeprojectacr2026.azurecr.io/video-deepfake-detector:latest \\
  --registry-server deepfakeprojectacr2026.azurecr.io \\
  --target-port 8000 --ingress external \\
  --min-replicas 1 --max-replicas 3 \\
  --cpu 2.0 --memory 4Gi

# 4. Update (new build)
az containerapp update --name deepfake-api \\
  --resource-group audio-deepfake-rg \\
  --image deepfakeprojectacr2026.azurecr.io/video-deepfake-detector:latest \\
  --revision-suffix fix1'''
    story.append(Preformatted(deploy_code, styles['CodeBlock']))
    story.append(PageBreak())

    # ========= 12. CONFIG REFERENCE =========
    story.append(Paragraph("12. Configuration Reference (config.yaml)", styles['STitle']))
    config_code = '''inference:
  frame_sample_rate: 3       # Frames per second to extract
  max_frames: 90             # Cap at 30 seconds (90 / 3)
  face_confidence: 0.5       # Face detection threshold
  real_threshold: 0.85       # prob_real >= this -> REAL
  fake_threshold: 0.25       # prob_real <= this -> FAKE
  pulse_override: 0.85       # Valid pulse -> min prob_real
  weights_dir: weights       # Path to model weight files

rppg:
  bandpass_low: 0.8          # Hz - lower bound for pulse filter
  bandpass_high: 3.0         # Hz - upper bound for pulse filter
  fps: 3                     # rPPG processing frame rate'''
    story.append(Preformatted(config_code, styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Parameter Tuning Guidelines:", styles['SubT']))
    tune_data = [
        ["<b>Parameter</b>", "<b>Default</b>", "<b>Effect of Increasing</b>", "<b>Effect of Decreasing</b>"],
        ["frame_sample_rate", "3", "More frames = slower, better rPPG", "Faster, less rPPG accuracy"],
        ["max_frames", "90", "Longer videos processed", "Shorter videos, faster response"],
        ["real_threshold", "0.85", "Fewer false positives", "More REAL verdicts"],
        ["fake_threshold", "0.25", "More FAKE verdicts", "Fewer false positives for FAKE"],
        ["pulse_override", "0.85", "Stronger pulse confirmation", "Weaker pulse influence"],
        ["bandpass_low", "0.8", "Filters out lower pulse rates", "Captures slower heart rates"],
        ["bandpass_high", "3.0", "Captures higher pulse rates", "More aggressive filtering"],
    ]
    story.append(add_table(tune_data[0], tune_data[1:], [90, 55, pw - 145, pw - 145]))
    story.append(PageBreak())

    # ========= 13. FILE MAP =========
    story.append(Paragraph("13. File-by-File Code Map", styles['STitle']))
    story.append(Paragraph(
        "Complete listing of every Python file in the project with its role and line count.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    file_data = [
        ["<b>File</b>", "<b>Lines</b>", "<b>Role</b>"],
        ["api.py", "158", "FastAPI server: POST /detect, GET /report/{id}, CORS, result cache"],
        ["detect.py", "~100", "CLI entry point: python detect.py video.mp4 [--json]"],
        ["report.py", "~400", "PDF report generator (ReportLab): badge, tables, charts, glossary"],
        ["download_models.py", "~30", "Downloads ResNet-18 + ViT-B/16 from HuggingFace at Docker build time"],
        ["config.yaml", "15", "Central configuration: thresholds, frame rate, rPPG params"],
        ["requirements.txt", "17", "Dependencies: torch, torchvision, opencv, fastapi, reportlab, neurokit2"],
        ["streams/face_detector.py", "~80", "FaceDetector class: OpenCV Haar cascade + MediaPipe fallback"],
        ["streams/visual_stream.py", "~60", "VisualStream class: ResNet-18 + ViT-B/16 wrapper"],
        ["streams/rppg_stream.py", "~120", "RPPGExtractor: CHROM/POS, bandpass filter, peak detection"],
        ["utils/video_io.py", "~50", "extract_frames(): VideoCapture, frame sampling, preprocess_face()"],
        ["utils/signal_proc.py", "~70", "butter_bandpass, find_peaks wrapper, compute_hrv with signal return"],
        ["fusion/build_features.py", "~40", "9-dim feature vector assembly + MinMaxScaler"],
        ["fusion/decision.py", "~100", "FusionEngine: weighted fusion + 5 override rules"],
        ["Dockerfile", "~40", "Multi-stage build: slim-bookworm, CPU PyTorch, HF model download"],
        [".dockerignore", "13", "Excludes venv, weights, mp4, pdf, git from Docker context"],
        [".gitignore", "15", "Excludes venv, pycache, mp4, pdf from git tracking"],
    ]
    story.append(add_table(file_data[0], file_data[1:], [120, 40, pw - 160]))
    story.append(PageBreak())

    # ========= 14. DEPENDENCY GRAPH =========
    story.append(Paragraph("14. Dependency Graph", styles['STitle']))
    story.append(Paragraph(
        "The import dependency structure of the project. Arrows mean 'imports from'.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))

    dep_code = '''api.py
  +-- utils/video_io.py     (extract_frames, preprocess_face)
  +-- streams/face_detector.py  (FaceDetector)
  +-- streams/visual_stream.py  (VisualStream)
  +-- streams/rppg_stream.py    (RPPGExtractor)
  +-- fusion/build_features.py  (build_feature_vector, FEATURE_NAMES)
  +-- fusion/decision.py        (FusionEngine)
  +-- report.py                 (generate_pdf)
  +-- config.yaml

visual_stream.py
  +-- torch, torchvision
  +-- utils/video_io.py     (preprocess_face)

rppg_stream.py
  +-- neurokit2             (CHROM, POS)
  +-- scipy.signal          (butter, sosfiltfilt, find_peaks)
  +-- scipy.stats           (kurtosis, skew)
  +-- numpy

decision.py
  +-- numpy
  +-- config.yaml

report.py
  +-- reportlab             (SimpleDocTemplate, Table, Paragraph, Image)
  +-- matplotlib            (figure, plot, savefig to BytesIO)
  +-- io (BytesIO)
  +-- base64'''
    story.append(Preformatted(dep_code, styles['CodeBlock']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("External Dependencies:", styles['SubT']))
    ext_data = [
        ["<b>Package</b>", "<b>Version</b>", "<b>License</b>", "<b>Purpose</b>"],
        ["torch", "2.x", "BSD", "Deep learning inference (CPU)"],
        ["torchvision", "0.x", "BSD", "Image preprocessing & transforms"],
        ["opencv-python", "4.x", "Apache 2.0", "Video I/O, face detection, image processing"],
        ["fastapi", "0.x", "MIT", "REST API framework"],
        ["uvicorn", "0.x", "BSD", "ASGI server"],
        ["reportlab", "4.x", "BSD", "PDF report generation"],
        ["matplotlib", "3.x", "BSD", "rPPG waveform chart rendering"],
        ["neurokit2", "0.x", "MIT", "rPPG (CHROM, POS) algorithms"],
        ["numpy", "1.x", "BSD", "Numerical computation"],
        ["scipy", "1.x", "BSD", "Signal filtering, peak detection, statistics"],
        ["scikit-learn", "1.x", "BSD", "MinMaxScaler for feature normalization"],
        ["pyyaml", "6.x", "MIT", "Config file parsing"],
        ["huggingface-hub", "0.x", "Apache 2.0", "Model weight download"],
    ]
    story.append(add_table(ext_data[0], ext_data[1:], [75, 40, 65, pw - 180]))
    story.append(Spacer(1, 20))

    story.append(Table([[""]], colWidths=[pw], style=TableStyle([
        ('LINEBELOW', (0, 0), (0, 0), 1, HexColor('#e2e8f0'))
    ])))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "DeepGuard v3.0.0 | Architecture & Implementation Guide | June 2026",
        styles['Footer']
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    create_impl_guide("Technical_Architecture_Guide.pdf")
