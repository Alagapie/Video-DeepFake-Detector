# DeepGuard: Real-Time Video Deepfake Detector

**Tagline:** *Dual-stream AI that detects synthetic faces by analyzing what cameras see — and what hearts reveal.*

---

## Description

### What It Does

DeepGuard is a production-ready deepfake detection API that analyzes videos using **two independent biological signals**: visual appearance and physiological pulse (rPPG). By fusing a computer vision model with a remote photoplethysmography (rPPG) pipeline, DeepGuard catches deepfakes that visual-only detectors miss — including frozen-face renders, lip-sync forgeries, and expression-swapped videos where the face looks real but carries no pulse signal.

The system exposes a FastAPI endpoint (`POST /detect`) where users upload a video and receive a JSON verdict — **REAL, FAKE, UNCERTAIN, or NO_FACE** — along with a downloadable PDF forensic report. It is deployed on Azure Container Apps, fully serverless and auto-scaling.

### Why It Matters

Synthetic video generation tools (HeyGen, EchoMimic, Diff2Lip, Sora) are now accessible to anyone with a browser. The line between authentic and fabricated video has blurred. Journalists, fact-checkers, platform moderators, and enterprise compliance teams need a **reliable, explainable, and scalable** tool to verify video authenticity — without requiring a GPU or a PhD in computer vision.

Existing deepfake detectors fall into two camps:
- **Visual-only models** (CNN/ViT classifiers) — vulnerable to adversarial frames, struggle with high-quality forgeries
- **End-to-end deep learning** (XGBoost on fused features) — brittle across datasets, requires retraining for every new generation of deepfakes

DeepGuard takes a third path: **physiological forensics**.

### How We Built It

**Architecture (Dual-Stream + Weighted Fusion):**

1. **Visual Stream (ResNet-18 + ViT-B/16)**
   - Face detection via OpenCV Haar cascade (zero GPU, zero protobuf conflicts)
   - Two pretrained models from Hugging Face (`abraraltaf92/deepfake-detection-models`) classify each frame
   - Per-model scores + temporal variance tracked across all frames

2. **rPPG Stream (CHROM + POS Algorithms)**
   - Skin-masked face ROIs fed through classical remote photoplethysmography
   - Bandpass filtering (0.8–3.0 Hz) isolates pulse from illumination noise
   - Heart rate (BPM), heart rate variability (RMSSD, SDNN), and waveform morphology (kurtosis, skewness, SNR) extracted

3. **Fusion Engine (Rule-Based Weighted Fusion)**
   - `0.6 × visual + 0.4 × rPPG` weighted score
   - Five deterministic physiological override rules that catch deepfakes without relying on learned correlations:
     - **Frozen-face rule:** temporal_std < 0.001 → immediate FAKE (physically impossible for a recording)
     - **Morphology rule:** kurtosis > 10 or < 0.5 + inflated HRV → immediate FAKE (deepfake pulse is spikey or flat)
     - **Low-SNR rule:** SNR < -2.0 + inflated HRV → immediate FAKE (noise masquerading as pulse)
     - **No-pulse cap:** prob_real capped at 0.70 without physiological confirmation
     - **Pulse override:** valid BPM (50–120) + good SNR → prob_real set to min 0.85

4. **API Layer (FastAPI)**
   - `POST /detect` — returns JSON verdict + `report_id`
   - `GET /report/{id}` — returns professional PDF (decision badge, color-coded metrics, rPPG waveform chart, face crop thumbnails, glossary appendix)
   - In-memory result cache with 10-minute TTL

5. **Deployment (Azure Container Apps)**
   - Multi-stage Docker build (slim-bookworm, CPU-only PyTorch)
   - Azure Container Registry build → Azure Container Apps (auto-scaling, auto-HTTPS, Consumption tier)
   - No VM management, no nginx, no cert renewal

**Stack:**
Python 3.10, PyTorch (CPU), torchvision, OpenCV, FastAPI, Uvicorn, ReportLab, Matplotlib, NeuroKit2, NumPy, SciPy, scikit-learn, Hugging Face Hub, Azure CLI, Docker

### Challenges We Ran Into

1. **XGBoost + SHAP brittleness.** The original design used XGBoost trained on Celeb-DF features with SHAP explainability. It failed catastrophically on out-of-distribution videos (e.g., Diff2Lip), learned dataset-specific correlations, and SHAP produced parse errors on unseen feature distributions. We replaced the entire fusion layer with weighted fusion + physiological rules — zero training required, perfectly transparent.

2. **rPPG at low frame rates.** Classical rPPG algorithms assume 30+ fps. At 3 fps (chosen for CPU feasibility), the Nyquist limit is 1.5 Hz (90 BPM). Bandpass filters crashed on edge cases. We added Wn clamping, minimum frame floors, and signal quality gates.

3. **Docker packaging on Debian trixie.** `libgl1-mesa-glx` was removed from Debian trixie (testing). We pinned to `slim-bookworm` (Debian 12 stable) and split pip install into two stages (CPU PyTorch from `download.pytorch.org/whl/cpu` first, then remaining packages from PyPI) because `--index-url` overrides all package resolution.

4. **CUDA kernel incompatibility on Kaggle.** Kaggle notebooks ship their own CUDA builds incompatible with pip-installed torch. Forced `device='cpu'` everywhere.

### Accomplishments We're Proud Of

- **Zero-training fusion engine** that outperforms our trained XGBoost on out-of-distribution deepfakes
- **Physiological override rules** that catch frozen-face, lip-sync, and expression-swap forgeries with perfect precision
- **Professional PDF reports** with color-coded metric tables, rPPG waveform charts, face crop thumbnails, and a plain-English glossary — accessible to non-technical stakeholders
- **Fully deployed on Azure** with HTTPS, auto-scaling, and CI/CD via ACR builds
- **No GPU required** for inference — runs on $0.08/hour Azure Consumption tier

### What We Learned

- Remote photoplethysmography works as a deepfake detector because **synthetic faces do not bleed** — even state-of-the-art generative models produce faces with no pulse, abnormal pulse morphology, or frozen texture
- Rule-based physiological forensics is more robust than ML-based fusion across unseen generator architectures — physical constraints don't overfit to training data
- Weighted fusion with explicit override rules is more explainable and trustworthy for high-stakes decisions than a black-box classifier
- Classical signal processing (bandpass filters, peak detection, kurtosis analysis) can compete with deep learning on physiological signals at a fraction of the compute cost

### What's Next

- **Multi-face support** — detect and analyze every face in a frame independently
- **Audio-rPPG cross-modal sync** — verify lip movement matches pulse timing
- **Adversarial patch testing** — benchmark robustness against face-swapping attacks
- **WebSocket streaming** — real-time deepfake detection for live video
- **Dashboard frontend** — companion React UI for non-API users

---

## Built With

- Python 3.10
- PyTorch (CPU)
- torchvision
- OpenCV (Haar Cascade)
- FastAPI
- Uvicorn
- ReportLab
- Matplotlib
- NeuroKit2
- NumPy
- SciPy
- scikit-learn
- Hugging Face Transformers
- Hugging Face Hub
- Hugging Face Models (`abraraltaf92/deepfake-detection-models`)
- ResNet-18
- Vision Transformer (ViT-B/16)
- CHROM (rPPG)
- POS (rPPG)
- Azure Container Registry
- Azure Container Apps
- Docker
- Docker Compose
- GitHub
- Git

---

## Human-in-the-Loop Design

**Decision NOT automated:** *Final verification of REAL verdicts involving public figures or sensitive content.*

**Why a human must remain in control:** DeepGuard's pulse override rule can raise `prob_real` to 0.85 when a valid BPM (50–120) with good SNR is detected. While this is a strong physiological signal, a motivated attacker could inject pulse-like noise into a deepfake video (e.g., rhythmic lighting flicker at ~1.2 Hz). For content involving public figures, political statements, or evidentiary material, a human analyst must review the rPPG waveform chart and face crop thumbnails in the PDF report before accepting a REAL verdict. The system is designed as a **decision support tool**, not an autonomous arbiter.

---

## Responsible AI Guardrail

**Risk:** *False positive harm — labeling authentic content as FAKE could erode trust in legitimate media (e.g., misclassifying a journalist's field recording as a deepfake).*

**Mitigation:** DeepGuard's three-way output (REAL / FAKE / UNCERTAIN) includes an **UNCERTAIN** verdict triggered when confidence is insufficient — specifically when rPPG data is unavailable and visual confidence falls below 0.85. The system refuses to guess. Additionally, every FAKE verdict includes a human-readable `reason` field explaining exactly which physiological rule triggered the decision. If the reason is "No face detected" or "Low signal quality", the user knows the result is unreliable and can seek a second opinion. The confidence score is always surfaced alongside the decision, allowing downstream systems to set their own thresholds based on risk tolerance.

---

## Tools & Data Disclosure

### AI Tools Used

All tools used are **free and open-source** unless noted otherwise:

- **PyTorch (CPU)** — MIT license, open-source. Model inference framework.
- **OpenCV** — Apache 2.0, open-source. Face detection via Haar cascade.
- **Hugging Face Transformers & Hub** — Apache 2.0, open-source. Model weight distribution and loading.
- **NeuroKit2** — MIT license, open-source. Physiological signal processing (rPPG CHROM/POS algorithms).
- **scikit-learn** — BSD license, open-source. Feature scaling utilities.
- **FastAPI** — MIT license, open-source. REST API framework.
- **ReportLab** — BSD license, open-source. PDF report generation.
- **Matplotlib** — BSD license, open-source. rPPG waveform chart rendering.
- **NumPy / SciPy** — BSD license, open-source. Numerical computation and signal filtering.
- **GitHub Copilot** — paid subscription (monthly). Code completion assistance during development.
- **Azure CLI** — MIT license, open-source. Cloud deployment infrastructure management.
- **Docker** — Apache 2.0, open-source. Containerization.
- **Pretrained Models** — `abraraltaf92/deepfake-detection-models` on Hugging Face (ResNet-18 + ViT-B/16). Free, open-weights, no license restrictions identified.

**No paid API services** (OpenAI, Google Cloud Vision, AWS Rekognition, etc.) are used in the inference pipeline.

### Data Sources

- **Celeb-DF (v2)** — The visual models were pretrained on the Celeb-DF v2 dataset (publicly available, academic use). Celeb-DF contains 590 real videos and 5,639 deepfake videos of celebrities. We did **not** train on this dataset — we use pretrained weights from Hugging Face.
- **Synthetic test videos** — Generated using:
  - **HeyGen** — AI avatar lip-sync platform (commercial). Used to create deepfake test samples.
  - **EchoMimic** — Open-source audio-driven portrait animation. Used for expression-swap deepfakes.
  - **Diff2Lip** — Open-source lip-sync diffusion model. Used for lip-sync forgery benchmarks.
- **Real webcam videos** — Authentic recordings captured locally for REAL verdict validation.
- **No external APIs or simulated data** were used for training or inference.

---

*Submitted to [Hackathon Name] — June 2026*
