# SLD Reader → Digital Twin → Asset Intelligence Platform

This repository contains a full-stack, deterministic, and explainable platform for converting Single Line Diagrams (SLDs) into a digital twin and running asset intelligence without external AI APIs.

## Architecture Overview

- **Backend**: FastAPI service with modular services for ingestion, digital twin building, time-series ingestion, intelligence, RCA, and reporting.
- **Frontend**: React + TypeScript dashboard for operator workflows.
- **Data**: SQLite for structured asset metadata and time-series storage (swap with production DB when deploying).

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the complete system design.

## Repository Layout

```
backend/
  app/
    api/            REST API routes
    core/           settings & configuration
    db/             schema + persistence
    models/         Pydantic models
    services/       ingestion, twin, intelligence, reporting
    workers/        background learning jobs
frontend/
  src/             React UI
config/            deployment configs
scripts/           helper scripts
```

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Train symbol classifier

Generate a synthetic dataset or provide curated crops under `data/symbols/<symbol_class>/*.png`. To generate an extensive synthetic dataset:

```bash
python scripts/generate_symbol_dataset.py --output data/symbols --samples 500
```

Then train the classifier:

```bash
python scripts/train_symbols.py --dataset data/symbols --output models/symbol_classifier.joblib
```

The trained model is loaded automatically by the vision service when present at `models/symbol_classifier.joblib`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Key Features Implemented

- SLD ingestion for images (with clear extension points for PDF/CAD parsing).
- Symbol detection + OCR pipelines (classical CV + Tesseract).
- Digital twin graph builder with unique IDs and connectivity.
- Multi-source time-series ingestion (CSV and API endpoints).
- Rule-based intelligence engine with explainable predictions.
- Incident capture and compliance-ready PDF reporting.
- SaaS-ready multi-tenant configuration model (see API models).

## Deployment Notes

- Replace the SQLite database with PostgreSQL for production deployments.
- Deploy backend with Uvicorn/Gunicorn behind a reverse proxy.
- Build frontend with `npm run build` and serve via CDN or static hosting.

## Testing

Tests can be added under `backend/tests` using `pytest`.
