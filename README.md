# Planner - Team Task Manager

A modern team task management application built with FastAPI and React 18.

## Quick Start

### Backend Setup (Python 3.11)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend running at: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend Setup (Node 16+)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend running at: http://localhost:3000

### Docker Setup

```bash
docker-compose up
```

## Testing

### Backend
```bash
cd backend
pytest                    # Run all tests
pytest --cov            # Run with coverage
pytest -v              # Verbose output
```

### Frontend
```bash
cd frontend
npm test                # Run tests
npm run test:coverage   # Run with coverage
```

## Linting & Formatting

### Backend
```bash
cd backend
black .                # Format with Black
flake8                 # Lint with Flake8
mypy .                 # Type checking
```

### Frontend
```bash
cd frontend
npm run lint           # Run ESLint
npm run lint:fix       # Fix ESLint issues
npm run format         # Format with Prettier
```

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM, JWT authentication
- **Frontend**: React 18 with React Router, Context API for state
- **Database**: SQLite (MVP) → PostgreSQL (production)
- **Testing**: pytest (backend), Jest (frontend)
- **Access Control**: Role-based (VIEWER, WORKER, ADMIN)

See [quickstart.md](./specs/001-team-task-manager/quickstart.md) for detailed setup instructions.
