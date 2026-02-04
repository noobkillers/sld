from pathlib import Path
from typing import List

import pandas as pd
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from app.db.database import Database
from app.models.schemas import (
    DigitalTwin,
    Equipment,
    Incident,
    IngestionResult,
    Prediction,
    ReportRequest,
    TimeseriesPoint,
)
from app.services.data_ingestion import ingest_csv
from app.services.digital_twin import DigitalTwinBuilder
from app.services.ingestion import ingest_document
from app.services.intelligence import IntelligenceEngine
from app.services.reporting import generate_pdf_report

router = APIRouter()

db = Database()


@router.post("/ingest/sld", response_model=IngestionResult)
async def ingest_sld(file: UploadFile = File(...)) -> IngestionResult:
    path = Path("/tmp") / file.filename
    contents = await file.read()
    path.write_bytes(contents)
    return ingest_document(path)


@router.post("/digital-twin", response_model=DigitalTwin)
async def build_digital_twin(equipment: List[Equipment]) -> DigitalTwin:
    builder = DigitalTwinBuilder()
    created = []
    for item in equipment:
        created.append(builder.add_equipment(item.name, item.equipment_type, item.rating))
    if len(created) >= 2:
        builder.connect(created[0], created[1])
    twin = builder.build()
    db.upsert_equipment(twin.equipment)
    db.add_connectivity(twin.connectivity)
    return twin


@router.post("/timeseries", response_model=List[TimeseriesPoint])
async def ingest_timeseries(points: List[TimeseriesPoint]) -> List[TimeseriesPoint]:
    db.add_timeseries(points)
    return points


@router.post("/timeseries/csv", response_model=List[TimeseriesPoint])
async def ingest_timeseries_csv(file: UploadFile = File(...)) -> List[TimeseriesPoint]:
    path = Path("/tmp") / file.filename
    contents = await file.read()
    path.write_bytes(contents)
    points = ingest_csv(str(path), source="csv")
    db.add_timeseries(points)
    return points


@router.post("/incidents", response_model=Incident)
async def create_incident(incident: Incident) -> Incident:
    db.add_incident(incident)
    return incident


@router.post("/predict", response_model=List[Prediction])
async def predict(equipment_id: str, industry: str) -> List[Prediction]:
    df = pd.DataFrame(
        [
            {"equipment_id": equipment_id, "metric": "thermal_loading", "value": 70.0},
            {"equipment_id": equipment_id, "metric": "thermal_loading", "value": 85.0},
        ]
    )
    engine = IntelligenceEngine(industry)
    anomalies = engine.detect_anomalies(df)
    prediction = engine.predict_rul(equipment_id, df)
    maintenance = engine.recommend_maintenance(prediction, anomalies)
    return [prediction, maintenance]


@router.post("/reports")
async def generate_report(request: ReportRequest) -> FileResponse:
    incidents: List[Incident] = []
    predictions: List[Prediction] = []
    report_path = generate_pdf_report(request.report_type, incidents, predictions)
    return FileResponse(report_path)
