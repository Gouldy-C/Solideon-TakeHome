## Frontend (React + Vite)

React dashboard for browsing weld groups, selecting layers, viewing 3D waypoints, and charting per‑layer metrics. Talks to the FastAPI backend at `http://127.0.0.1:8000/api` by default (`src/lib/api.ts`).

### Requirements
- Node.js 20+
- npm 10+

If Node.js isn't installed, download the LTS version (includes npm):

- Node.js downloads: https://nodejs.org/en/download/

### Install & run (dev)
```powershell
cd frontend
npm install
npm run dev
```

- Dev server: `http://localhost:5173`
- Ensure the backend is running on `http://127.0.0.1:8000` or update `src/lib/api.ts` accordingly.

### Build & preview
```powershell
npm run build
npm run preview
```

### Environment & configuration
- API base URL is hardcoded in `src/lib/api.ts`:
  - `baseURL: "http://127.0.0.1:8000/api"`
  - If you change backend host/port, update this string.
- Vite dev port is set to 5173 in `vite.config.ts`.

### Features
- Groups list with search and ingest status.
- Group detail page with layer selector, 3D view of waypoints, and charts.
- Upload ZIP modal to trigger backend ingestion (`/api/ingest/upload-zip`).

### Routes
- `/` → groups list
- `/group/:groupId` → group details

### Scripts
- `npm run dev` – start Vite dev server
- `npm run build` – type‑check and build for production
- `npm run preview` – preview production build
- `npm run lint` – run ESLint

### Tech
- React 19, TypeScript, Vite 7
- Tailwind CSS v4, Radix UI primitives
- TanStack Router + TanStack Query
- Recharts, Three.js via @react-three/fiber/@react-three/drei

