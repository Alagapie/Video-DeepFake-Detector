import io
import base64
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, Color, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage,
)

PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
SUCCESS = HexColor("#2ecc71")
WARNING = HexColor("#f39c12")
INFO = HexColor("#3498db")
GRAY = HexColor("#95a5a6")
BG_LIGHT = HexColor("#f8f9fa")
BORDER = HexColor("#dee2e6")
RED_BG = HexColor("#fde8e8")
GREEN_BG = HexColor("#e8fde8")
YELLOW_BG = HexColor("#fef9e7")


def _assess(metric, value):
    ranges = {
        "bpm": ((50, 120, SUCCESS), (30, 150, WARNING), (None, None, ACCENT)),
        "snr": ((0, None, SUCCESS), (-2, 0, WARNING), (None, -2, ACCENT)),
        "kurt": ((1.5, 4.0, SUCCESS), (0.5, 10.0, WARNING), (None, None, ACCENT)),
        "hrv_rmssd": ((20, 80, SUCCESS), (10, 150, WARNING), (None, None, ACCENT)),
        "hrv_sdnn": ((30, 120, SUCCESS), (15, 200, WARNING), (None, None, ACCENT)),
        "temporal_std": ((0.1, None, SUCCESS), (0.01, 0.1, WARNING), (None, 0.01, ACCENT)),
    }
    default = ("—", GRAY)
    if metric not in ranges:
        return default
    for lo, hi, color in ranges[metric]:
        above_lo = lo is None or value >= lo
        below_hi = hi is None or value < hi
        if above_lo and below_hi:
            if color == SUCCESS:
                return "Normal", color
            elif color == WARNING:
                return "Borderline", color
            else:
                return "Anomalous", color
    return default


def _baseline(metric):
    bl = {
        "bpm": "50–120 bpm", "snr": "> 0 dB", "kurt": "1.5–4.0",
        "hrv_rmssd": "20–80 ms", "hrv_sdnn": "30–120 ms", "temporal_std": "> 0.10",
    }
    return bl.get(metric, "—")


def _make_chart(signal, peaks, fps=3):
    fig, ax = plt.subplots(figsize=(6.2, 1.8))
    x = np.arange(len(signal)) / fps
    ax.plot(x, signal, color="#1a1a2e", linewidth=0.8)
    if len(peaks) > 0:
        ax.scatter(x[peaks], signal[peaks], color="#e94560", s=12, zorder=3)
    ax.set_xlabel("Time (s)", fontsize=7)
    ax.set_ylabel("BVP Amplitude", fontsize=7)
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout(pad=1.2)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130)
    plt.close(fig)
    buf.seek(0)
    return RLImage(buf, width=150*mm, height=40*mm)


def _make_table(data, col_widths=None, highlights=None):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    style = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), BG_LIGHT))
    if highlights:
        for (row, col, bg_color) in highlights:
            if row < len(data) and col < len(data[row]):
                style.append(("BACKGROUND", (col, row), (col, row), bg_color))
                style.append(("FONTNAME", (col, row), (col, row), "Helvetica-Bold"))
    t.setStyle(TableStyle(style))
    return t


def _section_header(text):
    return Paragraph(
        f"<font size='12' color='{PRIMARY.hexval()}'><b>{text}</b></font>",
        ParagraphStyle("H2", fontSize=12, spaceBefore=10, spaceAfter=4),
    )


def _metadata_footer():
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        ["Pipeline Version", "v3.0.0"],
        ["Execution Time", now],
        ["Face Tracking", "OpenCV Haar Cascade"],
        ["Visual Models", "ResNet-18 + ViT-B/16"],
        ["rPPG Core", "CHROM + POS (averaged)"],
        ["Visual Sampling", "3.0 fps"],
        ["Hardware", "CPU"],
    ]
    t = Table(
        [[Paragraph(f"<font size='7' color='{GRAY.hexval()}'><b>{r[0]}</b>: {r[1]}</font>",
                    ParagraphStyle("meta", fontSize=7))] for r in lines],
        colWidths=[150*mm], hAlign="LEFT",
    )
    t.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ]))
    return t


def generate_pdf(result, xai_data=None):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
    )
    story = []

    color, label, icon = _build_decision_badge(result["decision"])

    title = Paragraph(
        f"<font color='{PRIMARY.hexval()}'>Deepfake Detection Report</font>",
        ParagraphStyle("Title", fontSize=22, spaceAfter=12, leading=28, alignment=TA_CENTER),
    )
    story.append(title)

    subtitle = Paragraph(
        f"<font size='9' color='{GRAY.hexval()}'>"
        f"Dual-Stream Analysis &nbsp;·&nbsp; ResNet-18 + ViT-B/16 &nbsp;·&nbsp; rPPG (CHROM/POS)</font>",
        ParagraphStyle("Sub", fontSize=9, spaceAfter=14, leading=14, alignment=TA_CENTER),
    )
    story.append(subtitle)
    story.append(Spacer(1, 5*mm))

    badge_style = ParagraphStyle("Badge", fontSize=24, leading=30, textColor=white, alignment=TA_CENTER)
    badge_content = Paragraph(f"<b>{icon}  {label}</b>", badge_style)
    badge = Table([[badge_content]], colWidths=[150*mm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(badge)
    story.append(Spacer(1, 3*mm))

    info_data = [
        ["Metric", "Value"],
        ["File", result["video"]],
        ["Decision", label],
        ["Confidence", f"{result['confidence']:.2%}"],
        ["Real Probability", f"{result['prob_real']:.2%}"],
        ["Reason Code", result.get("reason", "N/A")],
    ]
    story.append(_section_header("Video Information"))
    story.append(_make_table(info_data, col_widths=[42*mm, 90*mm]))
    story.append(Spacer(1, 4*mm))

    vis_data = [["Model", "Score", "Assessment"]]
    vis_highlights = []
    vis_data.append(["ResNet-18", f"{result['per_model_scores'].get('resnet18', 0):.4f}", "—"])
    vis_data.append(["ViT-B/16", f"{result['per_model_scores'].get('vit_b16', 0):.4f}", "—"])
    vis_data.append(["Ensemble (avg)", f"{result['visual_score']:.4f}", "—"])
    ts = result["temporal_std"]
    ts_label, ts_color = _assess("temporal_std", ts)
    vis_data.append(["Temporal σ", f"{ts:.4f}", ts_label])
    if ts_color != SUCCESS:
        vis_highlights.append((4, 2, ts_color))
    story.append(_section_header("Visual Stream"))
    story.append(_make_table(vis_data, col_widths=[42*mm, 42*mm, 42*mm], highlights=vis_highlights))
    story.append(Spacer(1, 4*mm))

    rppg_data = [["Metric", "Value", "Baseline", "Assessment"]]
    rppg_highlights = []
    for idx, key in enumerate(["bpm", "snr", "kurt", "hrv_rmssd", "hrv_sdnn", "bpm_var"]):
        val = result["rppg"].get(key, 0)
        label_name, label_color = _assess(key, val)
        baseline_str = _baseline(key)
        formatted = f"{val}"
        row_idx = idx + 1
        rppg_data.append([key.upper(), formatted, baseline_str, label_name])
        if label_color != SUCCESS:
            rppg_highlights.append((row_idx, 3, label_color))
    story.append(_section_header("rPPG Physiological Stream"))
    story.append(_make_table(rppg_data, col_widths=[32*mm, 32*mm, 38*mm, 32*mm], highlights=rppg_highlights))
    story.append(Spacer(1, 4*mm))

    if xai_data and len(xai_data.get("filtered_signal", [])) > 5:
        story.append(_section_header("rPPG Waveform (Filtered BVP)"))
        sig = np.array(xai_data["filtered_signal"])
        peaks = np.array(xai_data.get("peaks", []), dtype=int)
        peaks = peaks[peaks < len(sig)]
        chart = _make_chart(sig, peaks, fps=3)
        story.append(chart)
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph(
            f"<font size='7' color='{GRAY.hexval()}'>Red dots indicate detected pulse peaks. "
            f"Spikey morphology or irregular spacing suggests synthetic generation.</font>",
            ParagraphStyle("caption", fontSize=7, spaceAfter=6, alignment=TA_CENTER),
        ))
        story.append(Spacer(1, 4*mm))

    if xai_data and len(xai_data.get("face_crops", [])) > 0:
        story.append(_section_header("Face Tracking"))
        crop_data = []
        for b64img in xai_data["face_crops"]:
            img_bytes = base64.b64decode(b64img)
            img_buf = io.BytesIO(img_bytes)
            rl_img = RLImage(img_buf, width=40*mm, height=40*mm)
            crop_data.append(rl_img)
        while len(crop_data) < 3:
            crop_data.append(Paragraph("", ParagraphStyle("empty", fontSize=1)))
        crop_table = Table([crop_data], colWidths=[45*mm, 45*mm, 45*mm])
        crop_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(crop_table)
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph(
            f"<font size='7' color='{GRAY.hexval()}'>First three detected face crops (resized for display).</font>",
            ParagraphStyle("caption", fontSize=7, spaceAfter=6, alignment=TA_CENTER),
        ))
        story.append(Spacer(1, 4*mm))

    if result.get("features"):
        feat_data = [["Feature", "Value", "Baseline", "Assessment"]]
        feat_highlights = []
        for idx, (k, v) in enumerate(result["features"].items()):
            bl = _baseline(k)
            lbl, lc = _assess(k, float(v))
            feat_data.append([k, f"{v}", bl, lbl])
            if lc != SUCCESS:
                feat_highlights.append((idx + 1, 3, lc))
        story.append(_section_header("Fusion Features"))
        story.append(_make_table(feat_data, col_widths=[32*mm, 32*mm, 38*mm, 32*mm], highlights=feat_highlights))
        story.append(Spacer(1, 4*mm))

    story.append(_section_header("Pipeline Metadata"))
    story.append(_metadata_footer())

    story.append(Spacer(1, 6*mm))
    story.append(_section_header("Metrics Reference Glossary"))
    glossary_entries = [
        ("Visual Score", "Baseline realism rating from the visual neural networks. High scores mean individual frames look photorealistic."),
        ("Temporal σ", "Frame-to-frame stability. Real faces have seamless micro-motion (σ > 0.10). Deepfakes often show unnaturally smooth or jittery pixel shifts."),
        ("BPM", "Heart rate estimated from remote photoplethysmography (rPPG) via micro colour changes in facial skin."),
        ("SNR", "Signal-to-noise ratio of the pulse extraction. Positive values mean a true cardiac pulse was isolated. Negative means the signal is mostly noise."),
        ("Kurtosis", "Pulse wave shape analysis. Normal human pulse: 1.5–4.0 (smooth). High values (>10) indicate jagged synthetic transitions typical of lip-sync deepfakes."),
        ("HRV (RMSSD/SDNN)", "Beat-to-beat time variation. Real pulse has moderate variability. Extremely inflated values (>200 ms) suggest the tracker is parsing algorithmic noise, not real blood flow."),
    ]
    gl_data = [["Term", "Plain English Definition"]]
    for term, defn in glossary_entries:
        gl_data.append([
            Paragraph(f"<font size='8'><b>{term}</b></font>", ParagraphStyle("gt", fontSize=8)),
            Paragraph(f"<font size='8'>{defn}</font>", ParagraphStyle("gd", fontSize=8, leading=11)),
        ])
    gl = Table(gl_data, colWidths=[32*mm, 110*mm], hAlign="LEFT")
    gl.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    for i in range(1, len(gl_data)):
        if i % 2 == 0:
            gl.setStyle(TableStyle([("BACKGROUND", (0, i), (-1, i), BG_LIGHT)]))
    story.append(gl)

    doc.build(story)
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes


def _build_decision_badge(decision):
    if decision == "REAL":
        return SUCCESS, "GENUINE", "✓"
    elif decision == "FAKE":
        return ACCENT, "MANIPULATED", "✗"
    elif decision == "UNCERTAIN":
        return WARNING, "INCONCLUSIVE", "?"
    return GRAY, "NO FACE", "—"
