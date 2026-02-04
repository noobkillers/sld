from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np


@dataclass
class TrainingSample:
    label: str
    image: np.ndarray


def load_symbol_dataset(root: Path) -> List[TrainingSample]:
    samples: List[TrainingSample] = []
    for label_dir in root.iterdir():
        if not label_dir.is_dir():
            continue
        label = label_dir.name
        for image_path in label_dir.glob("*.png"):
            image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue
            samples.append(TrainingSample(label=label, image=image))
    if not samples:
        raise ValueError(f"No training samples found in {root}")
    return samples


def augment_image(image: np.ndarray) -> List[np.ndarray]:
    augmented = [image]
    augmented.append(cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE))
    augmented.append(cv2.rotate(image, cv2.ROTATE_180))
    augmented.append(cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE))
    augmented.append(cv2.GaussianBlur(image, (3, 3), 0))
    return augmented


def build_feature_matrix(samples: List[TrainingSample]) -> Tuple[np.ndarray, List[str]]:
    hog = cv2.HOGDescriptor(
        _winSize=(64, 64),
        _blockSize=(16, 16),
        _blockStride=(8, 8),
        _cellSize=(8, 8),
        _nbins=9,
    )
    features = []
    labels: List[str] = []
    for sample in samples:
        for image in augment_image(sample.image):
            resized = cv2.resize(image, (64, 64))
            vector = hog.compute(resized).flatten()
            features.append(vector)
            labels.append(sample.label)
    return np.array(features), labels
