# System Architecture

## End-to-End Flow

1. **SLD Ingestion**
   - Accepts images, PDFs, and CAD (DWG/DXF).
   - Normalizes drawings into raster/graph formats.
   - Preserves scale and coordinate references for downstream extraction.

2. **Symbol & Text Extraction**
   - Classical CV for line/shape detection.
   - In-house OCR (Tesseract/PaddleOCR) for labels and ratings.
   - Output normalized symbol + label map.

3. **Digital Twin Core**
   - Equipment is assigned UUID + semantic ID.
   - Topology modeled as a directed graph.
   - Stores asset metadata (ratings, manufacturer, criticality).

4. **Data Ingestion**
   - SCADA, historian, relay event logs, tests, maintenance, and environment.
   - Time-series data indexed by equipment ID.

5. **Intelligence Engine**
   - Rule engine for thresholds.
   - Statistical trend analysis and anomaly detection.
   - Graph-based impact analysis.
   - Learning engine stores prediction outcomes and recalibrates thresholds.

6. **Incident & RCA**
   - Timeline reconstruction and root-cause mapping.
   - Cause → effect → impact chain.

7. **Reporting & Compliance**
   - PDF + JSON reports.
   - Filters by time and equipment.

8. **SaaS Model**
   - Multi-tenant configuration.
   - Subscription tiers mapped to feature flags.

## Services Breakdown

| Service | Responsibility |
| --- | --- |
| ingestion | SLD ingestion & normalization |
| vision | Symbol detection |
| ocr | Text extraction |
| digital_twin | Equipment graph builder |
| data_ingestion | CSV/API data ingestion |
| intelligence | Rules, anomaly detection, RUL prediction |
| reporting | PDF/JSON report generation |

## Deployment

- Containerize backend + frontend separately.
- Use background workers for scheduled learning and RCA tasks.
- Object storage for raw SLD uploads and derived assets.
