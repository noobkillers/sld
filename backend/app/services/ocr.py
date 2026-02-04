from typing import List, Dict, Any

import cv2
import numpy as np
import pytesseract


def extract_text(image: np.ndarray) -> List[Dict[str, Any]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10)
    data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
    results: List[Dict[str, Any]] = []
    for i, text in enumerate(data.get("text", [])):
        if not text.strip():
            continue
        results.append(
            {
                "text": text.strip(),
                "bbox": [
                    int(data["left"][i]),
                    int(data["top"][i]),
                    int(data["width"][i]),
                    int(data["height"][i]),
                ],
                "confidence": float(data["conf"][i]) if data["conf"][i] != "-1" else 0.0,
            }
        )
    return results
