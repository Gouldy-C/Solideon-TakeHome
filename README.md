## Solidion TakeHome — AM Spatial Sensing Analytics

A small full‑stack app for ingesting additive‑manufacturing run data and visualizing per‑layer metrics. The backend exposes a FastAPI `/api` for groups, layers, and ingestion of zipped `scandata`/`welddat` logs; the frontend is a React + Vite dashboard with charts and a simple 3D scene.

### Tech stack
- **Backend**: FastAPI (Pydantic v2), SQLModel/SQLAlchemy, SQLite, Uvicorn
- **Frontend**: React 19, TypeScript, Vite 7, Tailwind CSS v4, TanStack Router, TanStack Query, Radix UI
- **Viz**: Recharts, Three.js via @react-three/fiber

### Repository layout
- `backend/`: FastAPI service and SQLite database (`app/database/ssa_dashboard.db`)
- `frontend/`: React dashboard (Vite dev server on port 5173)

### Quick start (Windows PowerShell)
Open two terminals—one for the API and one for the UI.

1) Backend API (http://127.0.0.1:8000)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirments.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If you feel like the backend is running too slowly. Run the API with more workers.
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
```

1) Frontend UI (http://localhost:5173)
```powershell
cd frontend
npm install
npm run dev
```

API docs: visit `http://127.0.0.1:8000/docs`.

If you change ports, make sure the backend CORS origin (`FRONTEND_ORIGIN`) matches the frontend URL, and update the frontend API base URL in `frontend/src/lib/api.ts` if needed.

### Ingesting data (brief)
You can use the UI to ingest new data by clicking the upload zip button in the top right.

or...

POST a zip containing paired files like `w001_scandata.txt` and `w001_welddat.txt` to the backend:
```bash
curl -X POST "http://127.0.0.1:8000/api/ingest/upload-zip" \
  -F zip_file=@path/to/data.zip \
  -F group_name=my_run
```

See `backend/README.MD` and `frontend/README.md` for detailed instructions.


