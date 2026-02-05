# Quickstart Guide: Team Task Manager

**Date**: 2026-02-05  
**Purpose**: Get the application running locally in under 10 minutes.

---

## Prerequisites

- **Python 3.11+** (backend)
- **Node.js 16+ and npm** (frontend)
- **Git** (to clone the repo)
- **SQLite3** (usually pre-installed on macOS/Linux)

---

## Project Layout

```
work-planner/
├── backend/               # FastAPI server
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/              # React SPA
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.example
├── specs/                 # Documentation (this feature)
│   └── 001-team-task-manager/
├── README.md
└── docker-compose.yml     # Optional: containerized setup
```

---

## Quick Start (Local Development)

### 1. Clone the Repository

```bash
git clone https://github.com/rmcmahon/work-planner.git
cd work-planner
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env

# Initialize database and seed admin user
python -m src.db.init_db

# Start the backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Backend is ready**: Open http://localhost:8000/docs to view the interactive OpenAPI documentation.

### 3. Frontend Setup (in a new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (copy from .env.example)
cp .env.example .env

# Start development server
npm start
```

**Expected output**:
```
Compiled successfully!

You can now view the application in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Frontend is ready**: Open http://localhost:3000 in your browser.

---

## First Use: Login & Create a Task

### 1. Login as Admin

- **Username**: `admin`
- **Password**: `p@ssw0rd!`

**Expected**: Redirected to dashboard; empty task list displayed.

### 2. Create a Task

1. Click **"New Task"** button (top right or in dashboard).
2. Fill in the form:
   - **Name**: "Welcome Task"
   - **Priority**: HIGH
   - **Owner**: admin
   - **Status**: NOT_BLOCKED
   - **Delivery Date**: (optional) select a future date
3. Click **"Create"**.

**Expected**: Task appears at the top of the dashboard (sorted by priority, then position).

### 3. Test Drag-and-Drop

1. Create another task with **Priority: LOW**.
2. Drag the LOW-priority task above the HIGH-priority task.
3. Refresh the page (or observe optimistic update).

**Expected**: Tasks reordered; dashboard reflects the new order.

### 4. Test Filtering

1. Click the **"Filters"** panel (left sidebar).
2. Select **Priority: HIGH**.
3. Observe: only HIGH-priority task is visible.
4. Clear filters (click **"Clear Filters"**).

**Expected**: All tasks reappear.

### 5. Create a Subtask

1. Create a new task: "Subtask Example", Priority: MEDIUM.
2. On the parent task (HIGH-priority "Welcome Task"), click **"Make Parent"** (or drag onto it).
3. The "Subtask Example" task is now indented under the parent.

**Expected**: Subtask displayed indented with visual hierarchy.

### 6. Test Role-Based Access (Admin Page)

1. Click **"Admin"** in the top navigation.
2. You should see the **Users** tab (admin-only feature).
3. Click **"Create User"**:
   - **Username**: `alice`
   - **Password**: `password123`
   - **Display Name**: Alice Worker
   - **Role**: WORKER
4. Click **"Create"**.

**Expected**: New user appears in the users list.

### 7. Test Worker Access

1. **Logout** (click profile menu → Logout).
2. **Login as alice**:
   - **Username**: `alice`
   - **Password**: `password123`
3. You should see the dashboard but **NOT** the Admin tab.
4. Try to **Create a Task**: the new task's owner defaults to alice.
5. Try to **Edit** a task owned by admin: should be prevented (403 Forbidden error).

**Expected**: WORKER role has limited permissions (can't edit others' tasks, can't access admin).

---

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest --cov=src tests/
```

**Expected**: All tests pass; coverage report displayed.

### Frontend Tests

```bash
cd frontend
npm test
```

**Expected**: Jest test suite runs; watch mode active (press 'q' to quit).

---

## Environment Configuration

### Backend (.env)

```
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=<random-32-character-string>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
FRONTEND_URL=http://localhost:3000
LOG_LEVEL=INFO
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_DEBUG=true
```

---

## Troubleshooting

### Backend fails to start with "database is locked"

**Cause**: Another process is using the SQLite database.  
**Solution**: 
```bash
# Kill any previous processes
pkill -f "uvicorn src.main"
# Delete the database and reinitialize
rm backend/app.db
python -m src.db.init_db
```

### Frontend shows "Cannot GET /"

**Cause**: Frontend server not running or API URL misconfigured.  
**Solution**: 
1. Verify frontend is running on port 3000: `npm start`
2. Check `.env` has correct `REACT_APP_API_URL`

### API returns 401 Unauthorized

**Cause**: JWT token expired or missing.  
**Solution**: 
1. Log out and log in again.
2. Check browser DevTools → Application → Local Storage; verify access_token exists.

### "CORS error" when frontend calls backend

**Cause**: Backend CORS policy not configured for frontend origin.  
**Solution**: 
1. Check `backend/src/main.py` has CORSMiddleware configured for `http://localhost:3000`.
2. If missing, add:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Docker Setup (Optional)

For containerized development/deployment:

```bash
# Build and run both services with docker-compose
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## Deploying to Production

### Backend

```bash
# Build and push Docker image
docker build -t myregistry/work-planner-backend:1.0.0 .
docker push myregistry/work-planner-backend:1.0.0

# Deploy with environment variables injected (e.g., PostgreSQL URL, SECRET_KEY)
```

### Frontend

```bash
# Build static assets
npm run build

# Serve via web server (nginx, Apache, or CDN)
# Set REACT_APP_API_URL to production backend URL
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   React SPA (Port 3000)                 │
│  LoginPage → DashboardPage → AdminPage                  │
│  (Context API for auth state)                           │
└──────────────────┬──────────────────────────────────────┘
                   │ (HTTPS/REST)
┌──────────────────▼──────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                 │
│  /api/v1/auth/* → JWT token management                  │
│  /api/v1/tasks/* → Task CRUD, filtering, ordering       │
│  /api/v1/admin/* → User, project management             │
└──────────────────┬──────────────────────────────────────┘
                   │ (SQL)
┌──────────────────▼──────────────────────────────────────┐
│          SQLite Database (app.db)                        │
│  Tables: user, task, project, task_audit                │
└─────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Customize**: Modify styles, colors, and branding in `frontend/src/styles/`.
2. **Add Features**: Extend task model, add notifications, real-time updates.
3. **Deploy**: Follow production checklist (secrets management, HTTPS, scaling).
4. **Monitor**: Set up logging, error tracking (e.g., Sentry), and performance monitoring.

---

## Support & Issues

- **GitHub Issues**: https://github.com/rmcmahon/work-planner/issues
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Frontend Dev Tools**: React DevTools browser extension

---

## Summary

✅ Backend running on `http://localhost:8000`  
✅ Frontend running on `http://localhost:3000`  
✅ Login with `admin` / `p@ssw0rd!`  
✅ Create, edit, filter, and reorder tasks  
✅ Manage users and roles via admin page  
✅ Tests passing; ready for development

**Ready to build! 🚀**
