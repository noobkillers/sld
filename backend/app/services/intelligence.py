from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd

from app.models.schemas import Prediction


@dataclass
class RuleThreshold:
    metric: str
    warning: float
    critical: float


DEFAULT_RULES = [
    RuleThreshold(metric="voltage_deviation", warning=3.0, critical=5.0),
    RuleThreshold(metric="current_imbalance", warning=8.0, critical=12.0),
    RuleThreshold(metric="thermal_loading", warning=80.0, critical=95.0),
]


class IntelligenceEngine:
    def __init__(self, industry: str) -> None:
        self.industry = industry
        self.rules = self._adjust_rules_for_industry(industry)

    def _adjust_rules_for_industry(self, industry: str) -> List[RuleThreshold]:
        if industry.lower() in {"solar", "wind"}:
            return [
                RuleThreshold(metric="voltage_deviation", warning=4.0, critical=6.0),
                RuleThreshold(metric="current_imbalance", warning=10.0, critical=15.0),
                RuleThreshold(metric="thermal_loading", warning=75.0, critical=90.0),
            ]
        return DEFAULT_RULES

    def detect_anomalies(self, timeseries: pd.DataFrame) -> Dict[str, List[str]]:
        anomalies: Dict[str, List[str]] = {}
        for rule in self.rules:
            metric_series = timeseries[timeseries["metric"] == rule.metric]
            if metric_series.empty:
                continue
            latest = metric_series.iloc[-1]["value"]
            if latest >= rule.critical:
                anomalies.setdefault(rule.metric, []).append("critical")
            elif latest >= rule.warning:
                anomalies.setdefault(rule.metric, []).append("warning")
        return anomalies

    def predict_rul(self, equipment_id: str, timeseries: pd.DataFrame) -> Prediction:
        degradation = timeseries[timeseries["metric"] == "thermal_loading"]["value"]
        if degradation.empty:
            predicted = 365.0
            confidence = 0.3
            reasoning = ["Insufficient thermal loading data; using default RUL."]
        else:
            slope = np.polyfit(range(len(degradation)), degradation.to_numpy(), 1)[0]
            predicted = max(30.0, 365.0 - slope * 10)
            confidence = min(0.9, 0.5 + abs(slope) / 10)
            reasoning = [f"Thermal loading trend slope={slope:.2f} informs degradation rate."]
        return Prediction(
            equipment_id=equipment_id,
            prediction_type="RUL",
            predicted_value=float(predicted),
            confidence=float(confidence),
            reasoning=reasoning,
            evidence={"metric": "thermal_loading"},
        )

    def recommend_maintenance(self, prediction: Prediction, anomalies: Dict[str, List[str]]) -> Prediction:
        recommendation = "preventive"
        if any("critical" in levels for levels in anomalies.values()):
            recommendation = "corrective"
        elif prediction.predicted_value < 90:
            recommendation = "predictive"
        return Prediction(
            equipment_id=prediction.equipment_id,
            prediction_type="maintenance",
            predicted_value=prediction.predicted_value,
            confidence=prediction.confidence,
            reasoning=prediction.reasoning + [f"Recommendation={recommendation}"],
            evidence={"anomalies": anomalies},
        )
