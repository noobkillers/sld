from typing import List, Dict, Any, Optional

import cv2
import numpy as np

from pathlib import Path

from app.core.config import settings
from app.services.symbol_classifier import SymbolClassifier


def detect_symbols(image: np.ndarray) -> List[Dict[str, Any]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    symbols = []
    classifier: Optional[SymbolClassifier] = None
    if settings.symbol_model_path:
        classifier_path = Path(settings.symbol_model_path)
        if classifier_path.exists():
            classifier = SymbolClassifier(str(classifier_path))
            classifier.load()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h < 100:
            continue
        symbol_type = "unknown"
        confidence = 0.6
        if classifier is not None:
            crop = image[y : y + h, x : x + w]
            prediction = classifier.predict(crop)
            symbol_type = prediction.label
            confidence = prediction.confidence
        symbols.append(
            {
                "bbox": [int(x), int(y), int(w), int(h)],
                "confidence": float(confidence),
                "symbol_type": symbol_type,
            }
        )
    return symbols
