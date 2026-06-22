import os
import torch
import torch.nn as nn
import torchvision.models as models
import timm
import numpy as np

from utils.video_io import preprocess_face


class ResNetVideoClassifier(nn.Module):
    def __init__(self, dropout=0.3):
        super().__init__()
        backbone = models.resnet18(weights=None)
        in_features = backbone.fc.in_features
        backbone.fc = nn.Identity()
        self.backbone = backbone
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, 2),
        )

    def forward(self, x):
        B, C, H, W = x.shape
        feats = self.backbone(x)
        return self.head(feats)


class ViTVideoClassifier(nn.Module):
    def __init__(self, dropout=0.2):
        super().__init__()
        self.backbone = timm.create_model("vit_base_patch16_224", pretrained=False, num_classes=0)
        in_features = self.backbone.num_features
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, 2),
        )

    def forward(self, x):
        feats = self.backbone(x)
        return self.head(feats)


def load_model(arch, weights_path, device):
    if arch == "resnet18":
        model = ResNetVideoClassifier()
    elif arch == "vit_b16":
        model = ViTVideoClassifier()
    else:
        raise ValueError(f"Unknown architecture: {arch}")

    data = torch.load(weights_path, map_location="cpu", weights_only=False)
    if isinstance(data, dict) and "state_dict" in data:
        model.load_state_dict(data["state_dict"])
    else:
        model.load_state_dict(data)

    model.to(device)
    model.eval()
    return model


class VisualStream:
    def __init__(self, weights_dir, device="cpu"):
        self.device = device
        self.models = {}
        self.model_names = []

        resnet_path = os.path.join(weights_dir, "resnet18_best.pth")
        vit_path = os.path.join(weights_dir, "vit_base_patch16_224_best.pth")

        if os.path.exists(resnet_path):
            self.models["resnet18"] = load_model("resnet18", resnet_path, device)
            self.model_names.append("resnet18")

        if os.path.exists(vit_path):
            self.models["vit_b16"] = load_model("vit_b16", vit_path, device)
            self.model_names.append("vit_b16")

        if not self.models:
            raise FileNotFoundError(
                "No pretrained models found in weights_dir. "
                "Run download_models.py first."
            )

    @torch.no_grad()
    def predict(self, face_crops):
        if len(face_crops) == 0:
            return 0.5, 0.0, {}

        tensors = [preprocess_face(crop) for crop in face_crops]
        batch = torch.from_numpy(np.stack(tensors)).to(self.device)

        per_model_scores = {}
        all_probs = []

        for name, model in self.models.items():
            logits = model(batch)
            probs = torch.softmax(logits, dim=1)[:, 0].cpu().numpy()
            per_model_scores[name] = float(np.mean(probs))
            all_probs.append(probs)

        ensemble_probs = np.mean(all_probs, axis=0)
        visual_score = float(np.mean(ensemble_probs))
        temporal_std = float(np.std(ensemble_probs))

        return visual_score, temporal_std, per_model_scores

    def to(self, device):
        self.device = device
        for model in self.models.values():
            model.to(device)
        return self
