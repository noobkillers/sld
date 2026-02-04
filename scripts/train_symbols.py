from __future__ import annotations

import argparse
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
sys.path.append(str(repo_root / "backend"))

import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

from app.services.symbol_training import build_feature_matrix, load_symbol_dataset


def train_model(dataset_path: Path, output_path: Path) -> None:
    samples = load_symbol_dataset(dataset_path)
    features, labels = build_feature_matrix(samples)
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels)
    model = LinearSVC()
    model.fit(features, encoded_labels)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "labels": encoder.classes_.tolist()}, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train symbol classifier for SLD icons.")
    parser.add_argument("--dataset", type=Path, required=True, help="Path to symbol dataset root.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("models/symbol_classifier.joblib"),
        help="Output path for trained model.",
    )
    args = parser.parse_args()
    train_model(args.dataset, args.output)


if __name__ == "__main__":
    main()
