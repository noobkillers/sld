from datetime import datetime
from pathlib import Path
from typing import List

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.core.config import settings
from app.models.schemas import Incident, Prediction


def generate_pdf_report(title: str, incidents: List[Incident], predictions: List[Prediction]) -> Path:
    Path(settings.reports_path).mkdir(parents=True, exist_ok=True)
    filename = f"{title.replace(' ', '_').lower()}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    report_path = Path(settings.reports_path) / filename
    c = canvas.Canvas(str(report_path), pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, 750, title)
    c.setFont("Helvetica", 10)
    y = 720
    c.drawString(72, y, f"Generated: {datetime.utcnow().isoformat()} UTC")
    y -= 20
    c.drawString(72, y, "Incidents")
    y -= 15
    for incident in incidents:
        c.drawString(72, y, f"{incident.timestamp} - {incident.summary}")
        y -= 12
    y -= 20
    c.drawString(72, y, "Predictions")
    y -= 15
    for prediction in predictions:
        c.drawString(72, y, f"{prediction.prediction_type}: {prediction.predicted_value}")
        y -= 12
    c.showPage()
    c.save()
    return report_path
