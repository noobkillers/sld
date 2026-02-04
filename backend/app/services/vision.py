from typing import List, Dict, Any

import cv2
import numpy as np


def detect_symbols(image: np.ndarray) -> List[Dict[str, Any]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    symbols = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h < 100:
            continue
        symbols.append({"bbox": [int(x), int(y), int(w), int(h)], "confidence": 0.6})
    return symbols
