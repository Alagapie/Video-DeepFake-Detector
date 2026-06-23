import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def box(x, y, w, h, color, label, sublabel='', text_color='white', fontsize=10, subsize=8):
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                        facecolor=color, edgecolor='#2d3748', linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2 + 0.08, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color)
        if sublabel:
            ax.text(x + w / 2, y + h / 2 - 0.25, sublabel, ha='center', va='center',
                    fontsize=subsize, color=text_color, style='italic')

    def arrow(x1, y1, x2, y2, label='', color='#718096'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.15, label, ha='center', va='bottom',
                    fontsize=8, color=color, fontweight='bold')

    ax.text(7, 9.7, 'DeepGuard Architecture - Dual-Stream Video Deepfake Detector',
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1a202c')

    # Layer 1: Input
    box(5.5, 8.2, 3, 0.7, '#48bb78', 'VIDEO INPUT', 'Upload (MP4, AVI, MOV)', fontsize=11)
    arrow(7, 8.2, 7, 7.4, 'Frame extraction @ 3 fps')

    # Layer 2: Face Detection
    box(5.5, 6.5, 3, 0.7, '#edf2f7', 'FACE DETECTION', 'OpenCV Haar Cascade / MediaPipe',
        text_color='#2d3748')
    arrow(7, 6.5, 7, 5.8)

    # Split arrows
    ax.annotate('', xy=(4.5, 5.0), xytext=(6, 5.8),
                arrowprops=dict(arrowstyle='->', color='#718096', lw=2))
    ax.annotate('', xy=(9.5, 5.0), xytext=(8, 5.8),
                arrowprops=dict(arrowstyle='->', color='#718096', lw=2))

    # Visual Stream
    box(1.5, 3.5, 5, 1.3, '#4299e1', 'VISUAL STREAM', 'ResNet-18 + ViT-B/16', fontsize=11)
    vis_items = ['Face crops per frame', 'Two pretrained models (HuggingFace)',
                 'ResNet: 512-dim features', 'ViT: 768-dim features',
                 'Per-model deepfake probability', 'Temporal variance tracking']
    for i, item in enumerate(vis_items):
        ax.text(4, 3.2 - i * 0.18, f'  \u2022 {item}', ha='left', va='center',
                fontsize=7.5, color='#ebf8ff')

    # rPPG Stream
    box(7.5, 3.5, 5, 1.3, '#ed8936', 'rPPG STREAM', 'CHROM + POS Algorithms', fontsize=11)
    rppg_items = ['Skin-masked face ROI extraction', 'CHROM: Chrominance-based pulse',
                  'POS: Plane Orthogonal to Skin', 'Butterworth bandpass (0.8-3.0 Hz)',
                  'Heart rate, HRV, SNR, kurtosis', 'Peak detection (SciPy find_peaks)']
    for i, item in enumerate(rppg_items):
        ax.text(10, 3.2 - i * 0.18, f'  \u2022 {item}', ha='left', va='center',
                fontsize=7.5, color='#fffaf0')

    # Feature Vector
    arrow(4, 3.5, 4, 2.4, '9 features')
    arrow(10, 3.5, 10, 2.4, '9 features')
    box(4, 1.8, 6, 0.6, '#e2e8f0', 'FEATURE VECTOR (9-dim)', '',
        text_color='#2d3748', fontsize=10)

    # Fusion Engine
    arrow(7, 1.8, 7, 1.0, '')
    box(3.5, 0.3, 7, 0.7, '#9f7aea', 'FUSION ENGINE',
        'Weighted Fusion + 5 Physiological Override Rules', fontsize=11)

    # Outputs
    arrow(7, 0.3, 7, -0.5)
    arrow(7, -0.5, 3, -1.2)
    arrow(7, -0.5, 11, -1.2)
    box(0.5, -2.0, 5, 0.8, '#fc8181', 'JSON RESPONSE', 'POST /detect -> JSON verdict', fontsize=11)
    box(8.5, -2.0, 5, 0.8, '#667eea', 'PDF FORENSIC REPORT', 'GET /report/{id} -> PDF download', fontsize=11)
    ax.text(3, -0.8, 'decision, confidence, reason, report_id',
            ha='center', va='center', fontsize=7, color='#718096')
    ax.text(11, -0.8, 'Badge, metrics, waveform chart, face crops',
            ha='center', va='center', fontsize=7, color='#718096')

    # Deployment note
    ax.add_patch(mpatches.FancyBboxPatch((1.5, -3.3), 11, 0.7,
                                          boxstyle="round,pad=0.1",
                                          facecolor='#38b2ac', edgecolor='#2d3748',
                                          linewidth=1, alpha=0.15))
    ax.text(7, -2.95, 'DEPLOYMENT: Docker -> Azure Container Registry -> Azure Container Apps (CPU, auto-scaling, HTTPS)',
            ha='center', va='center', fontsize=9, color='#234e52', fontweight='bold')

    plt.tight_layout()
    plt.savefig('architecture_diagram.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Architecture diagram saved.")


def draw_decision_flowchart():
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis('off')

    def box(x, y, w, h, color, label, sublabel='', text_color='white', fontsize=9, subsize=7):
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                        facecolor=color, edgecolor='#2d3748', linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2 + 0.06, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color)
        if sublabel:
            ax.text(x + w / 2, y + h / 2 - 0.2, sublabel, ha='center', va='center',
                    fontsize=subsize, color=text_color, style='italic')

    def arrow(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#4a5568', lw=1.8))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            offset = 0.15 if abs(y2 - y1) > 0.5 else -0.15
            ax.text(mx + offset, my, label, ha='center', va='center',
                    fontsize=8, color='#4a5568', fontweight='bold')

    def dashed_arrow(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#4a5568', lw=1.5, linestyle='dashed'))

    ax.text(6, 11.6, 'Decision Engine Flow - Priority Order',
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1a202c')

    # START
    box(4.5, 10.5, 3, 0.7, '#48bb78', 'START', 'Features arrive from fusion', fontsize=10)

    # Rule 1
    y = 9.3
    box(4, y, 4, 0.65, '#4299e1', 'RULE 1: No face detected?')
    arrow(6, y + 0.65, 6, y + 1.2)
    arrow(6, y, 1.5, y - 0.5, 'YES')
    arrow(6, y, 10.5, y - 0.5, 'NO')
    box(0, y - 0.9, 3, 0.55, '#ecc94b', 'NO_FACE', '"No face detected"', text_color='#744210')

    # Rule 2
    y = 7.5
    box(4, y, 4, 0.65, '#4299e1', 'RULE 2: temporal_std < 0.001?')
    arrow(10.5, y + 0.65, 10.5, y + 1.6)
    arrow(10.5, y, 10.5, y - 0.5, 'NO')
    arrow(6, y, 1.5, y - 0.5, 'YES (frozen)')
    box(0, y - 0.9, 3, 0.55, '#fc8181', 'FAKE', '"Frozen face"')

    # Rule 3
    y = 5.7
    box(4, y, 4, 0.65, '#4299e1', 'RULE 3: Abnormal kurtosis?', fontsize=8)
    arrow(10.5, y, 10.5, y - 0.5, 'NO')
    arrow(6, y, 1.5, y - 0.5, 'YES (kurt>10 or kurt<0.5 + HRV)')
    box(0, y - 0.9, 3, 0.55, '#fc8181', 'FAKE', '"Abnormal rPPG morphology"')

    # Rule 4
    y = 3.9
    box(4, y, 4, 0.65, '#4299e1', 'RULE 4: Low SNR + high HRV?', fontsize=8)
    arrow(10.5, y, 10.5, y - 0.5, 'NO')
    arrow(6, y, 1.5, y - 0.5, 'YES (SNR<-2 + HRV)')
    box(0, y - 0.9, 3, 0.55, '#fc8181', 'FAKE', '"Low rPPG signal quality"')

    # Rule 5
    y = 2.1
    box(4, y, 4, 0.65, '#4299e1', 'RULE 5: No rPPG data?')
    arrow(10.5, y, 10.5, y - 0.5, 'NO')
    arrow(6, y, 1.5, y - 0.5, 'YES')
    box(0, y - 0.9, 3, 0.55, '#ecc94b', 'UNCERTAIN', '"No physiological confirmation"', text_color='#744210')

    # Rule 6: Normal fusion
    y = 0.3
    box(4, y, 4, 0.65, '#4299e1', 'RULE 6: Normal weighted fusion', fontsize=8)
    arrow(10.5, y, 10.5, y - 0.5, '')

    # Final outputs
    box(9, -0.8, 3, 0.55, '#fc8181', 'FAKE', 'prob_real < 0.25', fontsize=9, subsize=7)
    box(9, -1.6, 3, 0.55, '#ecc94b', 'UNCERTAIN', 'prob_real 0.25-0.85', fontsize=9, subsize=7, text_color='#744210')
    box(9, -2.4, 3, 0.55, '#48bb78', 'REAL', 'prob_real >= 0.85', fontsize=9, subsize=7)

    # Pulse override
    box(9, 0.5, 3, 0.6, '#f6e05e', 'PULSE OVERRIDE',
        'If BPM 50-120 + SNR > 0\nprob_real = max(0.85, prob_real)',
        text_color='#744210', fontsize=7, subsize=6.5)
    dashed_arrow(9.5, -0.25, 10.5, 0.5)

    plt.tight_layout()
    plt.savefig('decision_flowchart.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Decision flowchart saved.")


def draw_deployment():
    fig, ax = plt.subplots(1, 1, figsize=(12, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    def box(x, y, w, h, color, label, text_color='white', fontsize=10):
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                        facecolor=color, edgecolor='#2d3748', linewidth=1.3, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color)

    def arrow(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#4a5568', lw=2))
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.2, label, ha='center', va='bottom',
                    fontsize=7.5, color='#4a5568', fontweight='bold')

    ax.text(6, 4.2, 'CI/CD Pipeline - GitHub -> ACR -> Azure Container Apps',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1a202c')

    box(0.5, 1.5, 2.5, 1.5, '#24292e', 'GITHUB REPO', text_color='white', fontsize=9)
    ax.text(0.5 + 2.5/2, 1.5 + 1.5/2 - 0.3, 'Source code + Dockerfile',
            ha='center', va='center', fontsize=7, color='#cbd5e0')
    arrow(3, 2.25, 4.5, 2.25, 'az acr build')

    box(4.5, 1.5, 2.5, 1.5, '#0078d4', 'ACR BUILD', text_color='white', fontsize=8)
    ax.text(4.5 + 2.5/2, 1.5 + 1.5/2 - 0.3, 'Multi-stage Docker build\nCPU PyTorch, HF models',
            ha='center', va='center', fontsize=7, color='#bee3f8')
    arrow(7, 2.25, 8.5, 2.25, 'az containerapp update')

    box(8.5, 1.0, 3, 2.5, '#00897b', 'AZURE CONTAINER APPS', text_color='white', fontsize=9)
    ax.text(10, 2.5, 'Auto-scaling (1-3 replicas)', ha='center', va='center', fontsize=7.5, color='white')
    ax.text(10, 2.1, 'Auto-HTTPS / TLS', ha='center', va='center', fontsize=7.5, color='white')
    ax.text(10, 1.7, '2 CPU / 4 GB RAM', ha='center', va='center', fontsize=7.5, color='white')
    ax.text(10, 1.3, 'Consumption tier', ha='center', va='center', fontsize=7.5, color='white')

    plt.tight_layout()
    plt.savefig('deployment_pipeline.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Deployment diagram saved.")


if __name__ == '__main__':
    draw_architecture()
    draw_decision_flowchart()
    draw_deployment()
