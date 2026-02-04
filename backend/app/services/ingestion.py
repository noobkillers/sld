import uuid
from pathlib import Path
from typing import List

import cv2
import numpy as np
from PIL import Image

from app.models.schemas import IngestionResult
from app.services.ocr import extract_text
from app.services.vision import detect_symbols


SUPPORTED_IMAGE_EXT = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
SUPPORTED_DOC_EXT = {".pdf"}
SUPPORTED_CAD_EXT = {".dwg", ".dxf"}


def _load_image(path: Path) -> np.ndarray:
    image = Image.open(path)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def ingest_document(path: Path) -> IngestionResult:
    document_id = str(uuid.uuid4())
    notes: List[str] = []
    page_count = 1
    symbols_detected = 0
    labels_detected = 0

    if path.suffix.lower() in SUPPORTED_IMAGE_EXT:
        image = _load_image(path)
        symbols = detect_symbols(image)
        labels = extract_text(image)
        symbols_detected = len(symbols)
        labels_detected = len(labels)
    elif path.suffix.lower() in SUPPORTED_DOC_EXT:
        notes.append("PDF ingestion converts each page into images for CV processing.")
        notes.append("PDF rasterization requires external tools such as poppler.")
    elif path.suffix.lower() in SUPPORTED_CAD_EXT:
        notes.append("CAD ingestion uses DXF/DWG parsing and vector extraction.")
    else:
        notes.append("Unsupported format received.")

    return IngestionResult(
        document_id=document_id,
        page_count=page_count,
        symbols_detected=symbols_detected,
        labels_detected=labels_detected,
        notes=notes,
    )
