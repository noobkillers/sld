from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Rating(BaseModel):
    kv: Optional[float] = None
    ka: Optional[float] = None
    mva: Optional[float] = None
    hz: Optional[float] = None


class Equipment(BaseModel):
    id: str
    semantic_id: str
    name: str
    equipment_type: str
    rating: Rating
    manufacturer: Optional[str] = None
    install_date: Optional[datetime] = None
    criticality: int = Field(ge=1, le=5)


class Connectivity(BaseModel):
    from_id: str
    to_id: str
    relation: str


class TimeseriesPoint(BaseModel):
    equipment_id: str
    timestamp: datetime
    metric: str
    value: float
    source: str


class Incident(BaseModel):
    id: str
    equipment_id: str
    timestamp: datetime
    severity: str
    summary: str
    root_cause: Optional[str] = None
    impact: Optional[str] = None
    recommendations: Optional[str] = None


class IngestionResult(BaseModel):
    document_id: str
    page_count: int
    symbols_detected: int
    labels_detected: int
    notes: List[str]


class DigitalTwin(BaseModel):
    equipment: List[Equipment]
    connectivity: List[Connectivity]


class Prediction(BaseModel):
    equipment_id: str
    prediction_type: str
    predicted_value: float
    confidence: float
    reasoning: List[str]
    evidence: Dict[str, Any]


class ReportRequest(BaseModel):
    equipment_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    report_type: str


class TenantConfig(BaseModel):
    tenant_id: str
    subscription_tier: str
    industry: str
    retention_days: int = 365
