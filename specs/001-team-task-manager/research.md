# Research & Clarifications: Team Task Manager

**Phase**: Phase 0 (Research)  
**Date**: 2026-02-05  
**Purpose**: Resolve technical unknowns and establish best practices for implementation decisions.

---

## 1. Authentication & JWT Strategy

**Unknown**: How to implement secure session/token management for MVP?

**Decision**: Use JWT (JSON Web Tokens) with refresh token pattern.

**Rationale**:
- Stateless: no session store needed, simplifies scaling.
- Standard industry practice for REST APIs.
- Libraries (Python Cryptography, PyJWT; frontend: js-cookie, axios interceptors) mature and well-tested.
- Supports role-based authorization header inspection.

**Alternatives Considered**:
- Session cookies: would require server-side session store (added complexity for MVP).
- OAuth2 / SSO: out of scope; spec calls for simple username/password only.

**Implementation Details**:
- Access token TTL: 1 hour (short-lived).
- Refresh token TTL: 7 days (long-lived); stored in HTTP-only cookies.
- Password hashing: bcrypt (via `python-passlib`).
- Token creation on login; refresh endpoint to obtain new access token without re-login.

---

## 2. Drag-and-Drop Library Selection

**Unknown**: Which library to use for drag-and-drop task reordering in React?

**Decision**: Use `react-beautiful-dnd` (library maintained by Atlassian).

**Rationale**:
- Production-grade: used at scale by Jira, Trello-like apps.
- Keyboard accessible out-of-the-box (WCAG 2.1 compliance).
- Smooth animations and performance optimized.
- Clear documentation and active community.
- Handles nested drag-drop (for subtasks) with minimal config.

**Alternatives Considered**:
- `react-dnd`: more flexible but steeper learning curve; overkill for MVP.
- HTML5 native drag-drop: lower-level; requires manual accessibility handling.
- Custom implementation: high maintenance burden; error-prone.

**Implementation Details**:
- Use `DragDropContext`, `Droppable`, and `Draggable` components.
- Persist reorder changes to backend via PATCH /tasks/:id on drop.
- Optimistic UI updates (frontend reorder immediately; roll back if backend fails).

---

## 3. Data Persistence & Database

**Unknown**: Which database to use for MVP?

**Decision**: SQLite for MVP; designed to upgrade to PostgreSQL in future releases.

**Rationale**:
- Zero external dependencies: dev/test/deploy simplicity.
- Sufficient for initial target scope (MVP: <500 tasks, <10 users expected).
- File-based: easy backup and local iteration.
- SQLAlchemy ORM abstracts DB layer; migration to PostgreSQL requires minimal code change.

**Alternatives Considered**:
- PostgreSQL: more features (JSON, full-text search); overkill for MVP; requires Postgres server setup.
- Firebase/Firestore: vendor lock-in; billing complexity; not self-hosted.
- MongoDB: schema-less; adds complexity for relational data (users, tasks, projects); not justified.

**Implementation Details**:
- SQLite file: `backend/app.db`.
- Use SQLAlchemy with `sqlite3` dialect.
- Migrations via Alembic (lightweight ORM migration tool).
- Seeding: `backend/src/db/init_db.py` creates default tables and provisions admin user on first run.

---

## 4. Testing Strategy: Test-First & Coverage

**Unknown**: How to implement test-first for this feature within the Constitution's testing standards?

**Decision**: Write tests before implementation for core logic; enforce 80% coverage for auth and task modules.

**Rationale**:
- Aligns with Constitution principle "Testing Standards (Test-First)".
- Capture expected behavior before implementation to prevent bugs.
- 80% coverage balances rigor with pragmatism (UI snapshot tests exempt; focus on logic).

**Test Breakdown**:
- **Backend (pytest)**:
  - `test_auth.py`: Login, token refresh, password validation, JWT verification.
  - `test_tasks.py`: CRUD operations, ordering/position logic, filtering (additive filters).
  - `test_roles.py`: Access control enforcement (viewer can't edit, worker can't delete others' tasks, admin can do all).
  - `conftest.py`: Fixtures for test DB, authenticated user, sample tasks.
- **Frontend (Jest + React Testing Library)**:
  - Component tests: TaskCard, TaskList, FilterPanel render and interactions.
  - Page tests: LoginPage login flow, DashboardPage filter/drag interactions.
  - API mocking: jest-mock-axios or msw (Mock Service Worker) for HTTP mocking.
  - Coverage target: >70% for user-facing logic.

**CI/CD Integration**:
- Run pytest + Jest on every PR.
- Fail build if coverage drops below target.
- Generate coverage reports (HTML + LCOV) for visibility.

---

## 5. API Design & REST Conventions

**Unknown**: How to design REST endpoints for tasks with ordering, filtering, and subtasks?

**Decision**: RESTful design with query parameters for filters and a dedicated reorder endpoint.

**Rationale**:
- Standard REST conventions for discoverability and compatibility with REST clients.
- Query parameters for stateless filtering (client-driven queries).
- Separate endpoint for reordering to avoid accidental overwrites of other fields.

**Endpoint Design**:

```
# Authentication
POST   /api/v1/auth/login          # { username, password } → { access_token, refresh_token }
POST   /api/v1/auth/refresh        # { refresh_token } → { access_token }
POST   /api/v1/auth/logout         # Invalidate token (optional for MVP)

# Tasks
GET    /api/v1/tasks               # Query filters: ?owner=user_id&priority=high&status=in_progress
POST   /api/v1/tasks               # { name, description, priority, owner_id, project_id, delivery_date, status }
GET    /api/v1/tasks/:id           # Fetch task details
PATCH  /api/v1/tasks/:id           # { name, description, priority, owner_id, project_id, delivery_date, status }
DELETE /api/v1/tasks/:id           # Soft delete or permanent (TBD)
POST   /api/v1/tasks/:id/parent    # { parent_task_id } → Set parent (make subtask)
PATCH  /api/v1/tasks/:id/position  # { position, target_list_id } → Reorder within list

# Admin
GET    /api/v1/admin/users         # List all users (admin only)
POST   /api/v1/admin/users         # { username, password, display_name, role }
PATCH  /api/v1/admin/users/:id     # { role, display_name, email }
DELETE /api/v1/admin/users/:id     # (TBD: soft delete recommended)
GET    /api/v1/admin/projects      # List projects
POST   /api/v1/admin/projects      # { name, metadata }
```

**Response Format**:
- Success: `{ status: "success", data: {...} }`.
- Error: `{ status: "error", message: "...", code: "ERROR_CODE" }`.
- Pagination (for future): `{ status: "success", data: [...], page: 1, total: 50 }`.

---

## 6. Frontend State Management

**Unknown**: Should we use Redux, Context API, or other state management?

**Decision**: React Context API + local component state for MVP. Upgrade to Redux if needed post-MVP.

**Rationale**:
- Context API sufficient for MVP scope (single dashboard, global auth state).
- Simpler mental model: no boilerplate.
- Easier onboarding for new developers.
- Redux migration straightforward if performance or feature complexity increases.

**Implementation**:
- `AuthContext.tsx`: Global auth state (user, roles, token).
- Local state in `DashboardPage.tsx` for filtered tasks, sort order, drag state.
- Lifting state only where needed (parent to siblings).

---

## 7. Accessibility & WCAG 2.1 AA Compliance

**Unknown**: How to ensure WCAG 2.1 AA compliance in MVP?

**Decision**: Use semantic HTML, follow ARIA guidelines, enforce keyboard navigation, and use automated testing.

**Rationale**:
- Constitution requires WCAG 2.1 AA as non-negotiable.
- Semantic HTML (`<button>`, `<form>`, `<label>`) provides baseline.
- Keyboard navigation (Tab, Enter, Escape) for all interactive elements.
- Automated tools catch color contrast and aria issues.

**Implementation**:
- Use native HTML form elements where possible (not custom `<div>` buttons).
- Every `input` has associated `<label>`.
- Color contrast ratio >4.5:1 for text (use contrast checker during design).
- Test with screen readers (NVDA, JAWS) — manual testing; automated: axe-core.
- Keyboard-only navigation test: verify all UI interactions without mouse.

**Tools**:
- `axe-core` (automated accessibility testing in Jest).
- `@testing-library/react` (encourage semantic queries by role, label, etc.).
- Lighthouse (Chrome DevTools) for accessibility audit before release.

---

## 8. Performance Profiling & Optimization Strategy

**Unknown**: How to ensure dashboard load <1s for 500 tasks?

**Decision**: Pagination/virtualization, indexed DB queries, and profiling benchmarks.

**Rationale**:
- Rendering 500 DOM nodes is slow; virtual scrolling shows only visible tasks.
- DB indexes on `owner_id`, `priority`, `status`, `delivery_date` for fast filtering.
- React DevTools Profiler to identify re-render bottlenecks.

**Implementation**:
- Backend: Indexes on Task table for filter columns. Query profiling with SQLAlchemy logging.
- Frontend: React.lazy() for code splitting; `react-window` for virtual scrolling if task count grows.
- Benchmark: Load 500 tasks locally; measure render time and API response time.
- Target: API response <200ms; frontend render <300ms.

---

## 9. Deployment & Environment Configuration

**Unknown**: How to handle environment-specific config (dev, test, prod)?

**Decision**: Use `.env` files with environment variables; sensible defaults for local dev.

**Rationale**:
- Avoids hardcoding secrets; follows twelve-factor app principles.
- Easy CI/CD integration: secrets injected at deploy time.

**Environment Variables**:
```
# Backend
DATABASE_URL=sqlite:///./app.db (dev) or postgresql://... (prod)
SECRET_KEY=<random-32-char-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
FRONTEND_URL=http://localhost:3000 (dev) or https://app.example.com (prod)

# Frontend
REACT_APP_API_URL=http://localhost:8000 (dev) or https://api.example.com (prod)
```

**Management**:
- `.env.example`: checked into git; no secrets.
- `.env.local`: gitignored; used by dev.
- CI/GitHub Secrets: stored secrets injected at build time.

---

## Summary: Unknowns Resolved ✅

| Unknown | Decision | Confidence | Notes |
|---------|----------|-----------|-------|
| Auth strategy | JWT + refresh token | High | Standard; mature libraries |
| Drag-drop lib | react-beautiful-dnd | High | Accessibility built-in |
| Database | SQLite → PostgreSQL | High | Staged upgrade path |
| Testing | Test-first, 80% coverage | High | Aligns with Constitution |
| API design | RESTful + query filters | High | Industry standard |
| State mgmt | Context API (MVP) | Medium | Redis if scaling needed |
| Accessibility | Semantic HTML + WCAG AA | High | Constitution requirement |
| Performance | Virtual scrolling + indexes | Medium | Profiling to validate |
| Configuration | .env files + env vars | High | Twelve-factor app |

---

**Next Step**: Proceed to Phase 1 (Design & Contracts) to generate `data-model.md`, API contracts, and `quickstart.md`.
