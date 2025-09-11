## Backend (FastAPI)

FastAPI service that ingests additive‑manufacturing data and exposes read APIs for groups, layers, and computed metrics. Uses SQLite via SQLModel/SQLAlchemy.

### Requirements
- Python 3.11+
- Windows PowerShell examples below

### Setup
```powershell
cd backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirments.txt
```

### Run
```powershell
$env:FRONTEND_ORIGIN = "http://localhost:5173"  # CORS allowed origin
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API base: `http://127.0.0.1:8000/api`
- Docs: `http://127.0.0.1:8000/docs`

### Configuration
- CORS origin: read from `FRONTEND_ORIGIN` (defaults to `http://localhost:5173`).
- Config loader: on startup, loads JSON from `app/config/v0.1/*.json` (e.g., `equations_vars.json`) via `app.utils.config_loader.init_load`.
- SQLite DB: `app/database/ssa_dashboard.db` with WAL mode enabled.

### Data ingestion
Upload a `.zip` that contains paired per‑layer text files following naming pattern `w<NNN>_scandata.txt` and `w<NNN>_welddat.txt` (case‑insensitive; extra files are ignored). The server extracts safely and creates a `WeldGroup`, `Layer`, `ScanData`, and `WeldData` rows.

Endpoint:
```http
POST /api/ingest/upload-zip  (202 Accepted)
Form fields:
  - zip_file: file (.zip)
  - group_name: string (unique per group)
```

Example:
```bash
curl -X POST "http://127.0.0.1:8000/api/ingest/upload-zip" \
  -F zip_file=@path/to/data.zip \
  -F group_name=my_run
```

Parsing formats:
- scandata line: `[ScanValue, Xpos, Ypos, Zpos, V]`
- welddat line: `[Feedrate, CurrentValue, VoltageValue, Xpos, Ypos, Zpos, TravelSpeed]`

### API overview
- `GET /api/groups` → list groups with counts and ingest status
- `GET /api/groups/{group_id}` → group details with layer list
- `GET /api/groups/{group_id}/data` → aggregated per‑group weld metrics, plus per‑layer summaries
- `GET /api/layers/{layer_id}` → layer metadata
- `GET /api/layers/{layer_id}/data` → layer scan points, weld data, and summary stats

Response models are defined in `app/database/schemas.py`.

### Project structure
- `app/main.py` – app factory, CORS, router registration
- `app/routers/` – groups, layers, ingest endpoints
- `app/services/` – ingest and compute logic
- `app/database/` – models, DB engine, schemas
- `app/utils/` – parsers, transforms, config loader

### Notes
- Database auto‑creates on first run if missing.
- Ingest runs in a background task; initial response returns `202` while processing.
- If port changes, ensure the frontend `baseURL` in `frontend/src/lib/api.ts` matches and set `FRONTEND_ORIGIN` accordingly.


