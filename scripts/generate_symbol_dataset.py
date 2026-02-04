from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def draw_breaker(image: np.ndarray) -> None:
    h, w = image.shape
    cv2.line(image, (10, h // 2), (w // 3, h // 2), 255, 2)
    cv2.line(image, (w // 3, h // 2 - 10), (w // 3 + 20, h // 2 + 10), 255, 2)
    cv2.line(image, (w // 3 + 20, h // 2 + 10), (w - 10, h // 2 + 10), 255, 2)


def draw_transformer(image: np.ndarray) -> None:
    h, w = image.shape
    cv2.circle(image, (w // 3, h // 2), 18, 255, 2)
    cv2.circle(image, (w // 3 + 40, h // 2), 18, 255, 2)
    cv2.line(image, (10, h // 2), (w // 3 - 18, h // 2), 255, 2)
    cv2.line(image, (w // 3 + 58, h // 2), (w - 10, h // 2), 255, 2)


def draw_bus(image: np.ndarray) -> None:
    h, w = image.shape
    cv2.rectangle(image, (10, h // 2 - 5), (w - 10, h // 2 + 5), 255, -1)


def draw_load(image: np.ndarray) -> None:
    h, w = image.shape
    pts = np.array([[w // 2, 15], [w - 20, h - 15], [20, h - 15]])
    cv2.polylines(image, [pts], isClosed=True, color=255, thickness=2)
    cv2.line(image, (w // 2, 15), (w // 2, h - 15), 255, 1)


def draw_source(image: np.ndarray) -> None:
    h, w = image.shape
    cv2.circle(image, (w // 2, h // 2), 20, 255, 2)
    cv2.line(image, (w // 2 - 10, h // 2), (w // 2 + 10, h // 2), 255, 2)
    cv2.line(image, (w // 2, h // 2 - 10), (w // 2, h // 2 + 10), 255, 2)


def draw_capacitor(image: np.ndarray) -> None:
    h, w = image.shape
    cv2.line(image, (w // 3, h // 2 - 20), (w // 3, h // 2 + 20), 255, 2)
    cv2.line(image, (w // 3 + 20, h // 2 - 20), (w // 3 + 20, h // 2 + 20), 255, 2)
    cv2.line(image, (10, h // 2), (w // 3, h // 2), 255, 2)
    cv2.line(image, (w // 3 + 20, h // 2), (w - 10, h // 2), 255, 2)


def draw_relay(image: np.ndarray) -> None:
    h, w = image.shape
    cv2.rectangle(image, (w // 3, h // 3), (w // 3 + 40, h // 3 + 40), 255, 2)
    cv2.line(image, (10, h // 2), (w // 3, h // 2), 255, 2)
    cv2.line(image, (w // 3 + 40, h // 2), (w - 10, h // 2), 255, 2)


def draw_ground(image: np.ndarray) -> None:
    h, w = image.shape
    cv2.line(image, (w // 2, 20), (w // 2, h // 2), 255, 2)
    cv2.line(image, (w // 2 - 20, h // 2), (w // 2 + 20, h // 2), 255, 2)
    cv2.line(image, (w // 2 - 15, h // 2 + 10), (w // 2 + 15, h // 2 + 10), 255, 2)
    cv2.line(image, (w // 2 - 10, h // 2 + 20), (w // 2 + 10, h // 2 + 20), 255, 2)


SYMBOL_DRAWERS = {
    "breaker": draw_breaker,
    "transformer": draw_transformer,
    "bus": draw_bus,
    "load": draw_load,
    "source": draw_source,
    "capacitor": draw_capacitor,
    "relay": draw_relay,
    "ground": draw_ground,
}


def generate_dataset(output_dir: Path, samples_per_class: int, seed: int) -> None:
    rng = np.random.default_rng(seed)
    for label, drawer in SYMBOL_DRAWERS.items():
        class_dir = output_dir / label
        class_dir.mkdir(parents=True, exist_ok=True)
        for idx in range(samples_per_class):
            image = np.zeros((128, 128), dtype=np.uint8)
            drawer(image)
            noise = rng.normal(0, 10, image.shape).astype(np.int16)
            noisy = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            angle = float(rng.integers(-10, 10))
            matrix = cv2.getRotationMatrix2D((64, 64), angle, 1.0)
            rotated = cv2.warpAffine(noisy, matrix, (128, 128), borderValue=0)
            filename = class_dir / f"{label}_{idx:04d}.png"
            cv2.imwrite(str(filename), rotated)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic SLD symbol dataset.")
    parser.add_argument("--output", type=Path, default=Path("data/symbols"))
    parser.add_argument("--samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generate_dataset(args.output, args.samples, args.seed)


if __name__ == "__main__":
    main()
