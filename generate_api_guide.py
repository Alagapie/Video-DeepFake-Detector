from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import HRFlowable
import textwrap


def create_api_guide_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        'CoverTitle', fontName='Helvetica-Bold', fontSize=28,
        leading=34, alignment=TA_CENTER, spaceAfter=12,
        textColor=HexColor('#1a365d')
    ))
    styles.add(ParagraphStyle(
        'CoverSub', fontName='Helvetica', fontSize=14,
        leading=18, alignment=TA_CENTER, spaceAfter=6,
        textColor=HexColor('#4a5568')
    ))
    styles.add(ParagraphStyle(
        'SectionTitle', fontName='Helvetica-Bold', fontSize=18,
        leading=22, spaceBefore=24, spaceAfter=10,
        textColor=HexColor('#1a365d')
    ))
    styles.add(ParagraphStyle(
        'SubTitle', fontName='Helvetica-Bold', fontSize=14,
        leading=18, spaceBefore=16, spaceAfter=6,
        textColor=HexColor('#2d3748')
    ))
    styles.add(ParagraphStyle(
        'Body', fontName='Helvetica', fontSize=10,
        leading=14, spaceAfter=6, alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        'InlineCode', fontName='Courier', fontSize=8,
        leading=11, spaceAfter=4, leftIndent=16,
        backColor=HexColor('#f7fafc'),
        borderWidth=1, borderColor=HexColor('#e2e8f0'),
        borderPadding=6
    ))
    styles.add(ParagraphStyle(
        'CodeBlock', fontName='Courier', fontSize=7.5,
        leading=10, spaceAfter=8, leftIndent=12,
        backColor=HexColor('#f7fafc'),
        borderWidth=1, borderColor=HexColor('#e2e8f0'),
        borderPadding=8,
    ))
    styles.add(ParagraphStyle(
        'BulletItem', fontName='Helvetica', fontSize=10,
        leading=14, spaceAfter=4, leftIndent=20,
        bulletIndent=8, bulletFontSize=10
    ))
    styles.add(ParagraphStyle(
        'TableCell', fontName='Helvetica', fontSize=9,
        leading=12, alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'TableHeader', fontName='Helvetica-Bold', fontSize=9,
        leading=12, alignment=TA_CENTER, textColor=white
    ))
    styles.add(ParagraphStyle(
        'Note', fontName='Helvetica-Oblique', fontSize=9,
        leading=12, spaceAfter=6, leftIndent=12,
        textColor=HexColor('#718096')
    ))
    styles.add(ParagraphStyle(
        'Endpoint', fontName='Courier-Bold', fontSize=11,
        leading=14, spaceBefore=8, spaceAfter=4,
        textColor=HexColor('#2b6cb0')
    ))
    styles.add(ParagraphStyle(
        'Footer', fontName='Helvetica', fontSize=7,
        leading=9, textColor=HexColor('#a0aec0'),
        alignment=TA_CENTER
    ))

    story = []
    page_width = A4[0] - 40 * mm

    # ==============================
    # COVER PAGE
    # ==============================
    story.append(Spacer(1, 80))
    story.append(Paragraph("DeepGuard API", styles['CoverTitle']))
    story.append(Paragraph("Video Deepfake Detection API", styles['CoverSub']))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="60%", thickness=2, color=HexColor('#2b6cb0')))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Frontend Integration Guide for Developers", styles['CoverSub']))
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"Version 3.0.0", styles['CoverSub']))
    story.append(Paragraph("June 2026", styles['CoverSub']))
    story.append(Spacer(1, 60))

    base_url = "https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io"

    info_data = [
        ["Base URL", base_url],
        ["API Type", "REST (JSON)"],
        ["Authentication", "None (CORS: allow_origins=[\"*\"])"],
        ["Format", "multipart/form-data (upload) / JSON (response)"],
        ["Report Format", "PDF (application/pdf)"],
    ]
    info_table = Table(info_data, colWidths=[120, page_width - 120])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#edf2f7')),
        ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#2d3748')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # ==============================
    # TABLE OF CONTENTS
    # ==============================
    story.append(Paragraph("Table of Contents", styles['SectionTitle']))
    story.append(Spacer(1, 8))
    toc_items = [
        "1. API Overview & Endpoints",
        "2. POST /detect — Upload & Analyze",
        "3. GET /report/{id} — Download PDF",
        "4. Response Fields Reference",
        "5. Decision Rules & Their Meanings",
        "6. Frontend Integration Examples",
        "7. Error Handling Guide",
        "8. Performance & Limitations",
        "9. CORS & Security",
        "10. Quick-Start Cheat Sheet",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['Body']))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # ==============================
    # 1. API OVERVIEW
    # ==============================
    story.append(Paragraph("1. API Overview & Endpoints", styles['SectionTitle']))
    story.append(Paragraph(
        "DeepGuard is a production-ready deepfake detection API that analyzes videos using "
        "two independent biological signals: <b>visual appearance</b> (ResNet-18 + ViT-B/16) and "
        "<b>physiological pulse</b> (rPPG via CHROM/POS algorithms). It returns a verdict with "
        "confidence scores, per-model breakdown, and a downloadable PDF forensic report.",
        styles['Body']
    ))

    endpoints_data = [
        [Paragraph("<b>Method</b>", styles['TableHeader']),
         Paragraph("<b>Endpoint</b>", styles['TableHeader']),
         Paragraph("<b>Description</b>", styles['TableHeader'])],
        ["GET", "/", "Health check. Returns {\"status\":\"ready\"}"],
        ["POST", "/detect", "Upload video → JSON verdict + report_id"],
        ["GET", "/report/{report_id}", "Download PDF forensic report"],
    ]
    ep_table = Table(endpoints_data, colWidths=[60, 130, page_width - 190])
    ep_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (1, 0), (1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
    ]))
    story.append(Spacer(1, 8))
    story.append(ep_table)
    story.append(PageBreak())

    # ==============================
    # 2. POST /detect
    # ==============================
    story.append(Paragraph("2. POST /detect — Upload & Analyze", styles['SectionTitle']))
    story.append(Paragraph("<b>Endpoint:</b> <font face='Courier'>POST /detect</font>", styles['Body']))
    story.append(Paragraph("<b>Content-Type:</b> <font face='Courier'>multipart/form-data</font>", styles['Body']))
    story.append(Paragraph("<b>Body Parameter:</b> <font face='Courier'>file</font> (the video file)", styles['Body']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Supported Formats", styles['SubTitle']))
    formats_data = [
        [Paragraph("<b>Format</b>", styles['TableHeader']),
         Paragraph("<b>Extension</b>", styles['TableHeader']),
         Paragraph("<b>Notes</b>", styles['TableHeader'])],
        ["MP4", ".mp4", "H.264 encoded, preferred"],
        ["AVI", ".avi", "May be larger file size"],
        ["MOV", ".mov", "QuickTime container"],
        ["WebM", ".webm", "VP8/VP9 codec"],
        ["FLV", ".flv", "Flash video"],
    ]
    fmt_table = Table(formats_data, colWidths=[80, 80, page_width - 160])
    fmt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
    ]))
    story.append(fmt_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("cURL Example", styles['SubTitle']))
    curl_code = 'curl -X POST \\\n  -F "file=@video.mp4" \\\n  https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io/detect'
    story.append(Preformatted(curl_code, styles['CodeBlock']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("JavaScript (fetch) Example", styles['SubTitle']))
    js_code = '''async function checkDeepfake(videoFile) {
  const formData = new FormData();
  formData.append('file', videoFile);

  const res = await fetch(
    'https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io/detect',
    { method: 'POST', body: formData }
  );

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Detection failed');
  }

  return await res.json();
}'''
    story.append(Preformatted(js_code, styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Python Example", styles['SubTitle']))
    py_code = '''import requests

url = "https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io/detect"

with open("video.mp4", "rb") as f:
    files = {"file": ("video.mp4", f, "video/mp4")}
    res = requests.post(url, files=files, timeout=180)

if res.status_code == 200:
    data = res.json()
    print(f"Decision: {data['decision']}")
    print(f"Reason: {data['reason']}")
    print(f"Report ID: {data['report_id']}")
else:
    print(f"Error {res.status_code}: {res.text}")'''
    story.append(Preformatted(py_code, styles['CodeBlock']))
    story.append(PageBreak())

    # ==============================
    # 3. GET /report/{id}
    # ==============================
    story.append(Paragraph("3. GET /report/{report_id} — Download PDF", styles['SectionTitle']))
    story.append(Paragraph(
        "After a successful detection, the API returns a <font face='Courier'>report_id</font> "
        "(8-character hex string). Use it to download a professional PDF forensic report.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Endpoint:</b> <font face='Courier'>GET /report/{report_id}</font>", styles['Body']))
    story.append(Paragraph("<b>Response:</b> <font face='Courier'>application/pdf</font> (binary download)", styles['Body']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("cURL Example", styles['SubTitle']))
    curl2_code = 'curl -o forensic_report.pdf \\\n  https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io/report/ee96c81b'
    story.append(Preformatted(curl2_code, styles['CodeBlock']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("JavaScript (Download Trigger) Example", styles['SubTitle']))
    js2_code = '''async function downloadReport(reportId) {
  const res = await fetch(
    `https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io/report/${reportId}`
  );

  if (!res.ok) {
    throw new Error('Report not found or expired');
  }

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `deepfake_report_${reportId}.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}'''
    story.append(Preformatted(js2_code, styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("PDF Report Contents", styles['SubTitle']))
    pdf_items = [
        "Decision badge (color-coded: green=REAL, red=FAKE, yellow=UNCERTAIN, gray=NO_FACE)",
        "Video file info (filename, duration, frame count)",
        "Visual stream metrics table (ResNet-18 + ViT-B/16 scores) with reference baselines",
        "rPPG stream metrics table (BPM, HRV, SNR, kurtosis) with color-coded health assessments",
        "rPPG waveform chart with detected pulse peaks (matplotlib-generated chart embedded as PNG)",
        "Face crop thumbnails (up to 3 sample frames)",
        "Fusion features table with color-coded highlights",
        "Pipeline metadata footer (model versions, inference time)",
        "Metrics Reference Glossary appendix (plain-English explanations of every metric)",
    ]
    for item in pdf_items:
        story.append(Paragraph(f"• {item}", styles['Bullet']))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Important:</b> Reports are cached in memory for <b>10 minutes</b> after detection. "
        "If the user downloads later, they must re-upload the video. The report_id expires "
        "after 10 minutes and returns 404.",
        styles['Note']
    ))
    story.append(PageBreak())

    # ==============================
    # 4. RESPONSE FIELDS
    # ==============================
    story.append(Paragraph("4. POST /detect — Complete Response Fields Reference", styles['SectionTitle']))
    story.append(Paragraph(
        "This is the full JSON response structure. Every field is explained below.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))

    # Response JSON
    resp_json = '''{
  "video": "echo_mimic.mp4",
  "decision": "FAKE",
  "confidence": 1.0,
  "prob_real": 0.0,
  "visual_score": 0.999,
  "temporal_std": 0.0006,
  "per_model_scores": {
    "resnet18": 0.998,
    "vit_b16": 1.0
  },
  "rppg": {
    "bpm": 0.0,
    "bpm_var": 0.0,
    "hrv_rmssd": 0.0,
    "hrv_sdnn": 0.0,
    "snr": 0.0,
    "skew": 0.0,
    "kurt": 0.0
  },
  "features": {
    "visual_score": 1.0,
    "temporal_std": 0.0,
    "bpm": 0.0,
    "bpm_var": 0.0,
    "hrv_rmssd": 0.0,
    "hrv_sdnn": 0.0,
    "snr": 0.0,
    "skew": 0.0,
    "kurt": 0.0
  },
  "reason": "Frozen face — temporal variance near zero",
  "report_id": "ee96c81b"
}'''
    story.append(Preformatted(resp_json, styles['CodeBlock']))
    story.append(Spacer(1, 8))

    # Field reference table
    fields_data = [
        [Paragraph("<b>Field</b>", styles['TableHeader']),
         Paragraph("<b>Type</b>", styles['TableHeader']),
         Paragraph("<b>Range</b>", styles['TableHeader']),
         Paragraph("<b>Description</b>", styles['TableHeader'])],

        [Paragraph("decision", styles['TableCell']),
         Paragraph("string", styles['TableCell']),
         Paragraph("REAL / FAKE / UNCERTAIN / NO_FACE", styles['TableCell']),
         Paragraph("Primary verdict. Use this for your UI badge/display.", styles['TableCell'])],

        [Paragraph("confidence", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 1.0", styles['TableCell']),
         Paragraph("How confident the system is in its decision.", styles['TableCell'])],

        [Paragraph("prob_real", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 1.0", styles['TableCell']),
         Paragraph("Raw probability the video is authentic human speech.", styles['TableCell'])],

        [Paragraph("reason", styles['TableCell']),
         Paragraph("string", styles['TableCell']),
         Paragraph("—", styles['TableCell']),
         Paragraph("Human-readable explanation of why the decision was reached. Display this in your UI.", styles['TableCell'])],

        [Paragraph("report_id", styles['TableCell']),
         Paragraph("string", styles['TableCell']),
         Paragraph("8-char hex", styles['TableCell']),
         Paragraph("Use with GET /report/{id} to download PDF. Expires after 10 minutes.", styles['TableCell'])],

        [Paragraph("visual_score", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 1.0", styles['TableCell']),
         Paragraph("Visual model score. 1.0 = definitely a deepfake. 0.0 = definitely real.", styles['TableCell'])],

        [Paragraph("temporal_std", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 1.0+", styles['TableCell']),
         Paragraph("Frame-to-frame pixel variance. Near 0 = frozen face (instant FAKE).", styles['TableCell'])],

        [Paragraph("per_model_scores.resnet18", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 1.0", styles['TableCell']),
         Paragraph("ResNet-18 individual score.", styles['TableCell'])],

        [Paragraph("per_model_scores.vit_b16", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 1.0", styles['TableCell']),
         Paragraph("ViT-B/16 individual score.", styles['TableCell'])],

        [Paragraph("rppg.bpm", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 200.0", styles['TableCell']),
         Paragraph("Estimated heart rate from facial pulse. 0 = no pulse detected.", styles['TableCell'])],

        [Paragraph("rppg.hrv_rmssd", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 500.0", styles['TableCell']),
         Paragraph("Heart rate variability (RMSSD). Higher = more natural variation.", styles['TableCell'])],

        [Paragraph("rppg.snr", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("-10.0 – 10.0+", styles['TableCell']),
         Paragraph("rPPG signal-to-noise ratio. Positive = good signal.", styles['TableCell'])],

        [Paragraph("rppg.kurt", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("0.0 – 50.0+", styles['TableCell']),
         Paragraph("Pulse waveform kurtosis. Normal ~3. Extreme values = abnormal morphology.", styles['TableCell'])],

        [Paragraph("features.*", styles['TableCell']),
         Paragraph("float", styles['TableCell']),
         Paragraph("Varies", styles['TableCell']),
         Paragraph("All 9 features normalized for the fusion engine. Not typically needed for frontend display.", styles['TableCell'])],
    ]
    fields_table = Table(fields_data, colWidths=[95, 55, 90, page_width - 240])
    fields_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('FONTNAME', (0, 0), (0, -1), 'Courier'),
        ('FONTNAME', (1, 0), (1, -1), 'Courier'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
    ]))
    story.append(fields_table)
    story.append(PageBreak())

    # ==============================
    # 5. DECISION RULES
    # ==============================
    story.append(Paragraph("5. Decision Rules & Their Meanings", styles['SectionTitle']))
    story.append(Paragraph(
        "The decision engine follows a strict priority order. Understanding these rules helps "
        "you interpret the <font face='Courier'>reason</font> field in the response.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))

    rules_data = [
        [Paragraph("<b>Priority</b>", styles['TableHeader']),
         Paragraph("<b>Condition</b>", styles['TableHeader']),
         Paragraph("<b>Decision</b>", styles['TableHeader']),
         Paragraph("<b>Reason String</b>", styles['TableHeader'])],

        ["1", "No face detected in any frame", "NO_FACE", "No face detected in any frame"],
        ["2", "temporal_std < 0.001", "FAKE", "Frozen face \u2014 temporal variance near zero"],
        ["3", "rPPG kurtosis > 10 or < 0.5 + inflated HRV", "FAKE", "Abnormal rPPG morphology \u2014 spikey or flat pulse"],
        ["4", "SNR < -2.0 + inflated HRV", "FAKE", "Low rPPG signal quality \u2014 noise masquerading as pulse"],
        ["5", "No rPPG data + prob_real < 0.85", "UNCERTAIN", "No physiological confirmation \u2014 insufficient evidence"],
        ["6", "Valid pulse (BPM 50\u2013120, SNR > 0) + prob_real >= 0.85", "REAL", "Standard weighted fusion + valid pulse override"],
        ["7", "Default weighted fusion", "REAL/FAKE/UNCERTAIN", "Standard weighted fusion"],
    ]
    rules_table = Table(rules_data, colWidths=[50, 170, 65, page_width - 285])
    rules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
    ]))
    story.append(rules_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("What to display for each decision:", styles['SubTitle']))
    ui_data = [
        [Paragraph("<b>Decision</b>", styles['TableHeader']),
         Paragraph("<b>UI Badge Color</b>", styles['TableHeader']),
         Paragraph("<b>Recommended Icon</b>", styles['TableHeader']),
         Paragraph("<b>Example Message</b>", styles['TableHeader'])],

        ["REAL", "#22c55e (Green)", "✓", "Likely authentic human video"],
        ["FAKE", "#ef4444 (Red)", "✗", "AI-generated or manipulated video detected"],
        ["UNCERTAIN", "#f59e0b (Amber)", "?", "Insufficient evidence — manual review needed"],
        ["NO_FACE", "#6b7280 (Gray)", "—", "No face detected in video"],
    ]
    ui_table = Table(ui_data, colWidths=[70, 110, 70, page_width - 250])
    ui_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Courier-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
    ]))
    story.append(ui_table)
    story.append(PageBreak())

    # ==============================
    # 6. FRONTEND EXAMPLES
    # ==============================
    story.append(Paragraph("6. Frontend Integration Examples", styles['SectionTitle']))

    story.append(Paragraph("React Component — Full Example", styles['SubTitle']))
    react_code = '''import React, { useState } from 'react';

const API_BASE = 'https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io';

const DECISION_COLORS = {
  REAL: '#22c55e',
  FAKE: '#ef4444',
  UNCERTAIN: '#f59e0b',
  NO_FACE: '#6b7280'
};

const DECISION_LABELS = {
  REAL: 'Real',
  FAKE: 'Fake',
  UNCERTAIN: 'Uncertain',
  NO_FACE: 'No Face'
};

function DeepfakeChecker() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE}/detect`, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Detection failed');
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!result?.report_id) return;
    const res = await fetch(`${API_BASE}/report/${result.report_id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `deepfake_report_${result.report_id}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: 24 }}>
      <h1>DeepGuard Detector</h1>

      <input
        type="file"
        accept="video/*"
        onChange={e => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? 'Analyzing...' : 'Check Video'}
      </button>

      {error && (
        <div style={{ color: '#ef4444', marginTop: 16 }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{
          marginTop: 24,
          padding: 16,
          borderRadius: 8,
          borderLeft: `4px solid ${DECISION_COLORS[result.decision]}`
        }}>
          <h2 style={{ fontSize: 24, margin: 0 }}>
            {DECISION_LABELS[result.decision]}
          </h2>

          <p style={{ color: '#718096', marginTop: 4 }}>
            {result.reason}
          </p>

          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 8,
            marginTop: 16,
            fontSize: 14
          }}>
            <div>
              Confidence: <strong>{(result.confidence * 100).toFixed(0)}%</strong>
            </div>
            <div>
              Visual Score: <strong>{(result.visual_score * 100).toFixed(0)}%</strong>
            </div>
            <div>
              Heart Rate: <strong>{result.rppg.bpm?.toFixed(0) || 'N/A'} BPM</strong>
            </div>
            <div>
              Temporal Variance: <strong>{result.temporal_std?.toFixed(4)}</strong>
            </div>
          </div>

          <div style={{ marginTop: 8, fontSize: 13, color: '#718096' }}>
            ResNet-18: {(result.per_model_scores.resnet18 * 100).toFixed(0)}% |
            ViT-B/16: {(result.per_model_scores.vit_b16 * 100).toFixed(0)}%
          </div>

          <button
            onClick={downloadReport}
            style={{
              marginTop: 16,
              padding: '8px 16px',
              background: '#2b6cb0',
              color: 'white',
              border: 'none',
              borderRadius: 4,
              cursor: 'pointer'
            }}
          >
            Download PDF Report
          </button>
        </div>
      )}
    </div>
  );
}'''
    story.append(Preformatted(react_code, styles['CodeBlock']))
    story.append(PageBreak())

    story.append(Paragraph("Vue.js Example (Composition API)", styles['SubTitle']))
    vue_code = '''<template>
  <div>
    <input type="file" accept="video/*" @change="onFileChange" />
    <button @click="upload" :disabled="!file || loading">
      {{ loading ? 'Analyzing...' : 'Check Video' }}
    </button>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="result" class="result-card">
      <h2 :style="{ color: colors[result.decision] }">
        {{ labels[result.decision] }}
      </h2>
      <p class="reason">{{ result.reason }}</p>
      <p>Confidence: {{ (result.confidence * 100).toFixed(0) }}%</p>
      <p>BPM: {{ result.rppg.bpm?.toFixed(0) || 'N/A' }}</p>
      <button @click="downloadReport">Download PDF Report</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const API_BASE = 'https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io';
const file = ref(null);
const loading = ref(false);
const result = ref(null);
const error = ref(null);
const colors = { REAL: '#22c55e', FAKE: '#ef4444', UNCERTAIN: '#f59e0b', NO_FACE: '#6b7280' };
const labels = { REAL: 'Real', FAKE: 'Fake', UNCERTAIN: 'Uncertain', NO_FACE: 'No Face' };

const onFileChange = (e) => { file.value = e.target.files[0]; };

const upload = async () => {
  if (!file.value) return;
  loading.value = true;
  error.value = null;
  result.value = null;

  try {
    const fd = new FormData();
    fd.append('file', file.value);
    const res = await fetch(`${API_BASE}/detect`, { method: 'POST', body: fd });
    if (!res.ok) throw new Error((await res.json()).detail);
    result.value = await res.json();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};

const downloadReport = async () => {
  if (!result.value?.report_id) return;
  const res = await fetch(`${API_BASE}/report/${result.value.report_id}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `deepfake_report_${result.value.report_id}.pdf`;
  a.click();
  URL.revokeObjectURL(url);
};
</script>'''
    story.append(Preformatted(vue_code, styles['CodeBlock']))
    story.append(PageBreak())

    # ==============================
    # 7. ERROR HANDLING
    # ==============================
    story.append(Paragraph("7. Error Handling Guide", styles['SectionTitle']))
    story.append(Paragraph(
        "Every error returns a JSON body with a <font face='Courier'>detail</font> field. "
        "Your frontend should always check <font face='Courier'>res.ok</font> before parsing the response.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))

    err_data = [
        [Paragraph("<b>Scenario</b>", styles['TableHeader']),
         Paragraph("<b>Status</b>", styles['TableHeader']),
         Paragraph("<b>Response</b>", styles['TableHeader']),
         Paragraph("<b>Frontend Action</b>", styles['TableHeader'])],

        ["No file uploaded", "400", '{"detail": "No file provided."}', "Show 'Please select a video file'"],
        ["Empty filename", "400", '{"detail": "No file provided."}', "Show 'Please select a video file'"],
        ["Cannot read video frames", "400", '{"detail": "Could not read video frames."}', "Show 'Unsupported video format or corrupted file'"],
        ["No face detected", "200", '{"decision": "NO_FACE", ...}', "Show gray badge with 'No face detected'"],
        ["Report expired", "404", '{"detail": "Report not found or expired."}', "Show 'Report expired. Please re-upload video.'"],
        ["Server error", "500", "Internal Server Error", "Show 'Server error. Try again.' + retry button"],
        ["Timeout (cold start)", "502/504", "Gateway Timeout", "Show 'First load takes ~60s. Please retry.'"],
    ]
    err_table = Table(err_data, colWidths=[90, 45, 160, page_width - 295])
    err_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (1, 0), (1, -1), 'Courier'),
        ('FONTNAME', (2, 0), (2, -1), 'Courier'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
    ]))
    story.append(err_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Recommended Error Handling Pattern", styles['SubTitle']))
    err_code = '''async function safeDetect(videoFile) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 180000);

  try {
    const fd = new FormData();
    fd.append('file', videoFile);

    const res = await fetch(
      'https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io/detect',
      { method: 'POST', body: fd, signal: controller.signal }
    );

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      const msg = body.detail || `Server error (${res.status})`;
      throw new Error(msg);
    }

    return await res.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Request timed out. The video may be too large.');
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}'''
    story.append(Preformatted(err_code, styles['CodeBlock']))
    story.append(PageBreak())

    # ==============================
    # 8. PERFORMANCE
    # ==============================
    story.append(Paragraph("8. Performance & Limitations", styles['SectionTitle']))

    perf_data = [
        [Paragraph("<b>Characteristic</b>", styles['TableHeader']),
         Paragraph("<b>Value</b>", styles['TableHeader']),
         Paragraph("<b>Notes</b>", styles['TableHeader'])],

        ["Cold start time", "~60 seconds", "First request after idle scales up replica"],
        ["Inference time (30s video)", "30\u201390 seconds", "CPU-only. Depends on video length."],
        ["Max video duration", "~30 seconds", "Configured: 90 frames at 3 fps"],
        ["Frame sample rate", "3 fps", "Nyquist limit: 90 BPM for rPPG"],
        ["Max file size", "~100 MB", "Container Apps default limit"],
        ["Concurrent requests", "Up to 3", "Max replicas configured"],
        ["Report cache TTL", "10 minutes", "After that, re-upload required"],
        ["Supported formats", "MP4, AVI, MOV, WebM, FLV", "H.264 recommended"],
    ]
    perf_table = Table(perf_data, colWidths=[110, 80, page_width - 190])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "<b>Recommendations for frontend:</b> Show a progress indicator/loading spinner during "
        "detection. Set a 180-second timeout on your fetch call. On first load of the day, "
        "consider a pre-warm ping (GET /) to start the container before the real request.",
        styles['Body']
    ))
    story.append(PageBreak())

    # ==============================
    # 9. CORS & SECURITY
    # ==============================
    story.append(Paragraph("9. CORS & Security", styles['SectionTitle']))
    story.append(Paragraph(
        "The API is configured with wide-open CORS for development flexibility:",
        styles['Body']
    ))
    story.append(Spacer(1, 4))

    cors_code = '''// Current CORS configuration:
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
expose_headers=["Content-Disposition"]'''
    story.append(Preformatted(cors_code, styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "This means any web origin can call the API from the browser. "
        "However, credentialed requests (<font face='Courier'>credentials: 'include'</font>, "
        "cookies, HTTP auth) will fail with CORS errors. If your frontend sends credentials, "
        "we need to switch to a specific origin list.",
        styles['Body']
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>If your dashboard sends credentials:</b>", styles['SubTitle']))
    story.append(Paragraph("Send me the list of origins that will make requests (e.g., "
                           "<font face='Courier'>['https://your-app.com']</font>), "
                           "and I will update the server configuration.", styles['Body']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>To test CORS in the browser:</b>", styles['SubTitle']))
    cors_test_code = '''// Open browser console and run:
fetch('https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io/', {
  method: 'GET'
}).then(r => console.log('CORS OK:', r.status))
  .catch(e => console.error('CORS ERROR:', e));'''
    story.append(Preformatted(cors_test_code, styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "If you see a response, CORS is working. If you get a CORS error in the console, "
        "inspect the browser's network tab for the exact error message.",
        styles['Body']
    ))
    story.append(PageBreak())

    # ==============================
    # 10. QUICK-START
    # ==============================
    story.append(Paragraph("10. Quick-Start Cheat Sheet", styles['SectionTitle']))
    story.append(Paragraph("Copy-paste ready:", styles['Body']))
    story.append(Spacer(1, 8))

    quick_code = '''// === 1. Upload video & get result ===
const API = 'https://deepfake-api.reddune-ee354d90.francecentral.azurecontainerapps.io';

async function detect(videoFile) {
  const fd = new FormData();
  fd.append('file', videoFile);
  const res = await fetch(`${API}/detect`, { method: 'POST', body: fd });
  return await res.json();
}

// === 2. Display result ===
function renderResult(data) {
  return {
    badge: data.decision,           // "REAL" | "FAKE" | "UNCERTAIN" | "NO_FACE"
    color: {                        // Badge colors
      REAL: '#22c55e',
      FAKE: '#ef4444',
      UNCERTAIN: '#f59e0b',
      NO_FACE: '#6b7280'
    }[data.decision],
    label: data.reason,             // Human-readable explanation
    confidence: data.confidence,    // 0-1
    reportId: data.report_id        // For PDF download
  };
}

// === 3. Download PDF report ===
async function download(reportId) {
  const res = await fetch(`${API}/report/${reportId}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `deepfake_report_${reportId}.pdf`;
  a.click();
  URL.revokeObjectURL(url);
}

// === 4. Check that the API is alive ===
async function health() {
  const res = await fetch(API);
  const data = await res.json();
  return data.status === 'ready';
}'''
    story.append(Preformatted(quick_code, styles['CodeBlock']))
    story.append(Spacer(1, 16))

    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#e2e8f0')))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "For questions or support, contact the backend team.",
        styles['Footer']
    ))
    story.append(Paragraph(
        "DeepGuard API v3.0.0 | June 2026",
        styles['Footer']
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    create_api_guide_pdf("API_Integration_Guide.pdf")
