from datetime import datetime
from typing import List

import pandas as pd

from app.models.schemas import TimeseriesPoint


def ingest_csv(path: str, source: str) -> List[TimeseriesPoint]:
    df = pd.read_csv(path)
    points: List[TimeseriesPoint] = []
    for _, row in df.iterrows():
        points.append(
            TimeseriesPoint(
                equipment_id=str(row["equipment_id"]),
                timestamp=datetime.fromisoformat(str(row["timestamp"])),
                metric=str(row["metric"]),
                value=float(row["value"]),
                source=source,
            )
        )
    return points
