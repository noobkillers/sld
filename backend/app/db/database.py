import json
import sqlite3
from pathlib import Path
from typing import Iterable

from app.core.config import settings
from app.models.schemas import Connectivity, Equipment, Incident, TimeseriesPoint


class Database:
    def __init__(self) -> None:
        self.db_path = settings.database_url.replace("sqlite:///", "")
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        schema_path = Path(__file__).with_name("schema.sql")
        schema_sql = schema_path.read_text()
        with self._connect() as conn:
            conn.executescript(schema_sql)

    def upsert_equipment(self, equipment: Iterable[Equipment]) -> None:
        with self._connect() as conn:
            for item in equipment:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO equipment
                    (id, semantic_id, name, equipment_type, rating_json, manufacturer, install_date, criticality)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item.id,
                        item.semantic_id,
                        item.name,
                        item.equipment_type,
                        json.dumps(item.rating.model_dump()),
                        item.manufacturer,
                        item.install_date.isoformat() if item.install_date else None,
                        item.criticality,
                    ),
                )

    def add_connectivity(self, connectivity: Iterable[Connectivity]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM connectivity")
            for link in connectivity:
                conn.execute(
                    "INSERT INTO connectivity (from_id, to_id, relation) VALUES (?, ?, ?)",
                    (link.from_id, link.to_id, link.relation),
                )

    def add_timeseries(self, points: Iterable[TimeseriesPoint]) -> None:
        with self._connect() as conn:
            for point in points:
                conn.execute(
                    """
                    INSERT INTO timeseries (equipment_id, timestamp, metric, value, source)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        point.equipment_id,
                        point.timestamp.isoformat(),
                        point.metric,
                        point.value,
                        point.source,
                    ),
                )

    def add_incident(self, incident: Incident) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO incidents
                (id, equipment_id, timestamp, severity, summary, root_cause, impact, recommendations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    incident.id,
                    incident.equipment_id,
                    incident.timestamp.isoformat(),
                    incident.severity,
                    incident.summary,
                    incident.root_cause,
                    incident.impact,
                    incident.recommendations,
                ),
            )
