from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from .models import knn_predict, mean_predict, ridge_predict

FEATURES = [
    "ionizable_ratio",
    "helper_ratio",
    "cholesterol_ratio",
    "peg_ratio",
    "np_ratio",
    "payload_length_nt",
    "particle_size_nm",
    "pdi",
]


def load_rows(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def vector(row: dict) -> list[float]:
    payload_flags = [
        1.0 if row["payload_type"] == "mRNA" else 0.0,
        1.0 if row["payload_type"] == "siRNA" else 0.0,
    ]
    return [float(row[name]) for name in FEATURES] + payload_flags


def mae(y_true: list[float], y_pred: list[float]) -> float:
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)


def r2(y_true: list[float], y_pred: list[float]) -> float:
    mean = sum(y_true) / len(y_true)
    ss_total = sum((value - mean) ** 2 for value in y_true)
    ss_res = sum((a - b) ** 2 for a, b in zip(y_true, y_pred))
    return 1.0 - ss_res / ss_total if ss_total else 0.0


def run_benchmark(rows: list[dict], knn_k: int = 3, ridge_alpha: float = 1.0) -> tuple[dict, list[dict]]:
    studies = sorted({row["study_id"] for row in rows})
    predictions: list[dict] = []
    for held_out in studies:
        train = [row for row in rows if row["study_id"] != held_out]
        test = [row for row in rows if row["study_id"] == held_out]
        train_x, train_y = [vector(row) for row in train], [float(row["transfection_pct"]) for row in train]
        test_x, test_y = [vector(row) for row in test], [float(row["transfection_pct"]) for row in test]
        model_predictions = {
            "mean": mean_predict(train_y, test_x),
            "knn": knn_predict(train_x, train_y, test_x, knn_k),
            "ridge": ridge_predict(train_x, train_y, test_x, ridge_alpha),
        }
        for model, values in model_predictions.items():
            for row, truth, prediction in zip(test, test_y, values):
                predictions.append(
                    {
                        "formulation_id": row["formulation_id"],
                        "held_out_study": held_out,
                        "model": model,
                        "y_true": truth,
                        "y_pred": round(prediction, 4),
                    }
                )

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in predictions:
        grouped[row["model"]].append(row)
    summary = {
        "protocol": "leave_one_study_out",
        "n_formulations": len(rows),
        "n_studies": len(studies),
        "models": {},
    }
    for model, items in sorted(grouped.items()):
        truth = [item["y_true"] for item in items]
        predicted = [item["y_pred"] for item in items]
        summary["models"][model] = {
            "mae": round(mae(truth, predicted), 4),
            "r2": round(r2(truth, predicted), 4),
        }
    return summary, predictions


def write_results(output_dir: str | Path, summary: dict, predictions: list[dict]) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with (output_dir / "predictions.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
