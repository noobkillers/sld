from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import cv2
import joblib
import numpy as np


@dataclass
class SymbolPrediction:
    label: str
    confidence: float


class SymbolClassifier:
    def __init__(self, model_path: str) -> None:
        self.model_path = Path(model_path)
        self.model = None
        self.labels: List[str] = []

    def load(self) -> None:
        payload = joblib.load(self.model_path)
        self.model = payload["model"]
        self.labels = payload["labels"]

    def extract_features(self, image: np.ndarray) -> np.ndarray:
        if image.ndim == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(image, (64, 64))
        hog = cv2.HOGDescriptor(
            _winSize=(64, 64),
            _blockSize=(16, 16),
            _blockStride=(8, 8),
            _cellSize=(8, 8),
            _nbins=9,
        )
        features = hog.compute(resized)
        return features.flatten()

    def predict(self, image: np.ndarray) -> SymbolPrediction:
        if self.model is None:
            raise RuntimeError("Symbol classifier model is not loaded.")
        features = self.extract_features(image).reshape(1, -1)
        scores = self.model.decision_function(features)
        if scores.ndim == 1:
            best_idx = int(np.argmax(scores))
            confidence = float(scores[best_idx])
        else:
            best_idx = int(np.argmax(scores[0]))
            confidence = float(scores[0][best_idx])
        return SymbolPrediction(label=self.labels[best_idx], confidence=confidence)

    def batch_predict(self, crops: List[np.ndarray]) -> List[SymbolPrediction]:
        return [self.predict(crop) for crop in crops]
