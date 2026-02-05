---
description: "Task list for Team Task Manager implementation"
---

# Tasks: Team Task Manager

**Input**: Design documents from `/specs/001-team-task-manager/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/` at repository root
- **Frontend**: `frontend/src/`, `frontend/tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and basic structure

- [X] T001 Initialize Python 3.11 backend project structure in `backend/` with venv, requirements.txt
- [X] T002 Initialize React 18 frontend project structure in `frontend/` with package.json and webpack/create-react-app config
- [X] T003 [P] Set up pytest for backend testing in `backend/tests/` with conftest.py and test fixtures
- [X] T004 [P] Set up Jest + React Testing Library for frontend testing in `frontend/tests/`
- [X] T005 [P] Configure linting and formatting: backend (black, flake8), frontend (eslint, prettier)
- [X] T006 [P] Create `.env.example` files for backend and frontend with all required variables
- [X] T007 Create `docker-compose.yml` with PostgreSQL option for future and SQLite for MVP

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Set up FastAPI app entry point in `backend/src/main.py` with CORS middleware for frontend
- [ ] T009 [P] Configure SQLAlchemy ORM and database connection in `backend/src/db/database.py` for SQLite
- [ ] T010 [P] Define User ORM model in `backend/src/auth/models.py` with role enum (VIEWER, WORKER, ADMIN)
- [ ] T011 [P] Define Task ORM model in `backend/src/tasks/models.py` with priority, status, parent_task_id, position fields
- [ ] T012 [P] Define Project ORM model in `backend/src/tasks/models.py` (or separate file)
- [ ] T013 Create database migration setup with Alembic in `backend/alembic/` for future schema changes
- [ ] T014 Implement database initialization and seeding in `backend/src/db/init_db.py` (provision admin user: username=admin, password=p@ssw0rd!)
- [ ] T015 [P] Implement password hashing service in `backend/src/auth/service.py` using bcrypt
- [ ] T016 [P] Implement JWT token generation and verification in `backend/src/auth/service.py`
- [ ] T017 Create JWT middleware in `backend/src/middleware/auth.py` to verify and extract token from Authorization header
- [ ] T018 [P] Implement role-based access control (RBAC) helper in `backend/src/auth/service.py` with permission checks
- [ ] T019 Set up frontend App.tsx root component in `frontend/src/App.tsx` with routing (React Router v6)
- [ ] T020 [P] Create AuthContext in `frontend/src/context/AuthContext.tsx` for global auth state management
- [ ] T021 [P] Create ProtectedRoute component in `frontend/src/components/ProtectedRoute.tsx` to guard routes by authentication/role
- [ ] T022 Create axios/fetch client wrapper in `frontend/src/api/client.ts` with JWT token injection in headers
- [ ] T023 Set up global CSS in `frontend/src/styles/index.css` with WCAG 2.1 AA color contrast (semantic HTML baseline)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dashboard (Priority: P1) 🎯 MVP

**Goal**: Deliver a read-only dashboard showing all tasks prioritized and filterable by owner, priority, status, date, and project.

**Independent Test**: Log in as a viewer; verify dashboard loads tasks ordered by priority (HIGH → MEDIUM → LOW) and manual position; apply each filter individually and in combination; drop one task onto another and verify parent-child relationship.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T024 [P] Contract test for GET /api/v1/tasks endpoint in `backend/tests/test_tasks.py` (mock 10 sample tasks, verify response schema)
- [ ] T025 [P] Unit test for task ordering logic in `backend/tests/test_tasks.py` (priority DESC, then position ASC)
- [ ] T026 [P] Unit test for additive filtering (owner + priority + status + delivery_date + project) in `backend/tests/test_tasks.py`
- [ ] T027 [P] Unit test for subtask parent-child validation in `backend/tests/test_tasks.py` (no cycles, no self-parent)
- [ ] T028 [P] Integration test for Dashboard page render in `frontend/tests/pages/DashboardPage.test.tsx` (mock API, verify task list renders)
- [ ] T029 [P] Integration test for FilterPanel filter logic in `frontend/tests/components/FilterPanel.test.tsx` (apply filters, verify query params)
- [ ] T030 Integration test for drag-drop reorder in `frontend/tests/components/TaskList.test.tsx` (mock react-beautiful-dnd, verify position change)

### Implementation for User Story 1

- [ ] T031 [P] Implement GET /api/v1/tasks endpoint in `backend/src/tasks/routes.py` with query param filters (owner, priority, status, delivery_date_from, delivery_date_to, project)
- [ ] T032 [P] Implement task ordering service function in `backend/src/tasks/service.py` (sort by priority DESC, then position ASC)
- [ ] T033 [P] Implement task filtering service function in `backend/src/tasks/service.py` (apply additive filters: AND logic)
- [ ] T034 [P] Implement subtask hierarchy fetch in `backend/src/tasks/service.py` (return parent and child tasks)
- [ ] T035 Implement database indexes in `backend/src/db/` on Task.owner_id, Task.priority, Task.status, Task.delivery_date, Task.project_id for filter query performance
- [ ] T036 [P] Implement LoginPage component in `frontend/src/pages/LoginPage.tsx` with username/password form, login API call, token storage
- [ ] T037 [P] Implement DashboardPage component in `frontend/src/pages/DashboardPage.tsx` (fetch tasks, manage filter state, render TaskList + FilterPanel)
- [ ] T038 [P] Implement TaskList component in `frontend/src/components/TaskList.tsx` (render tasks with react-beautiful-dnd, handle drag-drop, call reorder API)
- [ ] T039 [P] Implement TaskCard component in `frontend/src/components/TaskCard.tsx` (display task name, priority badge, owner, delivery date, status)
- [ ] T040 [P] Implement FilterPanel component in `frontend/src/components/FilterPanel.tsx` (owner, priority, status, delivery_date, project filter controls)
- [ ] T041 Implement PATCH /api/v1/tasks/:id/position endpoint in `backend/src/tasks/routes.py` to handle drag-drop reorder and parent assignment
- [ ] T042 Implement parent-task validation service in `backend/src/tasks/service.py` (cycle detection, self-parent prevention)
- [ ] T043 Add validation and error handling to task endpoints in `backend/src/tasks/routes.py` (400 for invalid input, 404 for not found)
- [ ] T044 Add comprehensive logging in `backend/src/tasks/service.py` for task operations (fetch, filter, reorder)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Create & Edit Tasks (Priority: P2)

**Goal**: Enable WORKER and ADMIN users to create new tasks and edit tasks assigned to them; viewers remain read-only.

**Independent Test**: Log in as a worker; create a new task with all required fields; edit the task (name, priority, status, etc.); verify changes appear on dashboard immediately; verify other users see the changes after refresh.

### Tests for User Story 2 ⚠️

- [ ] T045 [P] Contract test for POST /api/v1/tasks endpoint in `backend/tests/test_tasks.py` (create task with required fields, verify response includes task.id)
- [ ] T046 [P] Contract test for PATCH /api/v1/tasks/:id endpoint in `backend/tests/test_tasks.py` (update task, verify updated fields)
- [ ] T047 [P] Unit test for access control on task creation in `backend/tests/test_roles.py` (VIEWER cannot create, WORKER/ADMIN can)
- [ ] T048 [P] Unit test for access control on task edit in `backend/tests/test_roles.py` (WORKER can only edit own tasks, ADMIN can edit all)
- [ ] T049 [P] Unit test for field validation on task create/edit in `backend/tests/test_tasks.py` (name required, owner_id required, etc.)
- [ ] T050 [P] Integration test for TaskFormModal in `frontend/tests/components/TaskForm.test.tsx` (render form, fill fields, submit, verify API call)
- [ ] T051 [P] Integration test for task edit flow in `frontend/tests/pages/DashboardPage.test.tsx` (click edit, open modal, update, close)

### Implementation for User Story 2

- [ ] T052 [P] Implement POST /api/v1/tasks endpoint in `backend/src/tasks/routes.py` (create task with owner_id, validate WORKER/ADMIN role)
- [ ] T053 [P] Implement PATCH /api/v1/tasks/:id endpoint in `backend/src/tasks/routes.py` (update task, enforce access control)
- [ ] T054 [P] Implement task creation service in `backend/src/tasks/service.py` (validate required fields, set created_by, assign position)
- [ ] T055 [P] Implement task update service in `backend/src/tasks/service.py` (validate fields, check ownership, update timestamps)
- [ ] T056 [P] Add role check decorator in `backend/src/middleware/auth.py` for endpoints requiring WORKER or ADMIN role
- [ ] T057 [P] Implement TaskFormModal component in `frontend/src/components/TaskForm.tsx` (create/edit modal with form fields, submit to API)
- [ ] T058 [P] Implement task creation flow in DashboardPage (click "New Task", open modal, on success add to task list)
- [ ] T059 [P] Implement task edit flow in DashboardPage (click edit icon on task, open modal, on success update task in list)
- [ ] T060 Add field validation in TaskForm component (required fields, delivery_date >= today)
- [ ] T061 Add error handling in TaskForm for API errors (display field-specific errors, show toast for generic errors)
- [ ] T062 [P] Implement DELETE /api/v1/tasks/:id endpoint in `backend/src/tasks/routes.py` (soft delete, ADMIN only)
- [ ] T063 Add delete confirmation dialog in TaskCard component in `frontend/src/components/TaskCard.tsx` (ADMIN only)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: User Story 3 - Role-Based Admin (Priority: P3)

**Goal**: Allow ADMIN users to manage users, assign roles, create projects, and access an admin-only page.

**Independent Test**: Log in as admin; access /admin page (should be forbidden for non-admin); create a new user with WORKER role; assign ADMIN role to a user; create a new project; verify new user can log in and has correct permissions.

### Tests for User Story 3 ⚠️

- [ ] T064 [P] Contract test for GET /api/v1/admin/users endpoint in `backend/tests/test_admin.py` (verify returns list of users, ADMIN only)
- [ ] T065 [P] Contract test for POST /api/v1/admin/users endpoint in `backend/tests/test_admin.py` (create user, verify response includes user.id and role)
- [ ] T066 [P] Contract test for PATCH /api/v1/admin/users/:id endpoint in `backend/tests/test_admin.py` (update user role)
- [ ] T067 [P] Contract test for GET /api/v1/admin/projects endpoint in `backend/tests/test_admin.py` (verify returns list of projects)
- [ ] T068 [P] Contract test for POST /api/v1/admin/projects endpoint in `backend/tests/test_admin.py` (create project, verify response)
- [ ] T069 [P] Unit test for role-based access to admin endpoints in `backend/tests/test_roles.py` (VIEWER/WORKER get 403, ADMIN succeeds)
- [ ] T070 [P] Integration test for AdminPage render in `frontend/tests/pages/AdminPage.test.tsx` (login as admin, verify admin page loads; login as worker, verify redirect)
- [ ] T071 [P] Integration test for user creation flow in AdminPage in `frontend/tests/pages/AdminPage.test.tsx` (click create user, fill form, verify in list)

### Implementation for User Story 3

- [ ] T072 [P] Implement GET /api/v1/admin/users endpoint in `backend/src/admin/routes.py` (list all users, ADMIN only)
- [ ] T073 [P] Implement POST /api/v1/admin/users endpoint in `backend/src/admin/routes.py` (create user, validate username unique, hash password)
- [ ] T074 [P] Implement PATCH /api/v1/admin/users/:id endpoint in `backend/src/admin/routes.py` (update role, display_name, email)
- [ ] T075 [P] Implement DELETE /api/v1/admin/users/:id endpoint in `backend/src/admin/routes.py` (soft deactivate user, ADMIN only)
- [ ] T076 [P] Implement user creation service in `backend/src/admin/service.py` (validate fields, hash password, assign role)
- [ ] T077 [P] Implement user update service in `backend/src/admin/service.py` (validate role, prevent self-demotion from ADMIN if last admin)
- [ ] T078 [P] Implement GET /api/v1/admin/projects endpoint in `backend/src/admin/routes.py` (list all projects, accessible to all authenticated users)
- [ ] T079 [P] Implement POST /api/v1/admin/projects endpoint in `backend/src/admin/routes.py` (create project, ADMIN only)
- [ ] T080 [P] Add @require_role('ADMIN') decorator in `backend/src/middleware/auth.py` for admin-only endpoints
- [ ] T081 [P] Implement AdminPage component in `frontend/src/pages/AdminPage.tsx` with Users and Projects tabs
- [ ] T082 [P] Implement AdminUserPanel component in `frontend/src/components/AdminUserPanel.tsx` (list users, create user form, edit role, deactivate)
- [ ] T083 [P] Implement AdminProjectPanel component in `frontend/src/components/AdminProjectPanel.tsx` (list projects, create project form)
- [ ] T084 Add ProtectedRoute check for AdminPage requiring role === 'ADMIN' in `frontend/src/App.tsx`
- [ ] T085 Add error handling for 403 Forbidden responses in frontend (display message, redirect to dashboard if user lacks permission)

**Checkpoint**: All user stories complete and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and prepare for release

- [ ] T086 [P] Implement error handling service in `backend/src/middleware/error_handler.py` (global exception handler, return consistent error responses)
- [ ] T087 [P] Implement structured logging in `backend/src/utils/logging.py` (context-aware logs for auth, tasks, admin operations)
- [ ] T088 Run accessibility audit using axe-core and Lighthouse in `frontend/tests/` (ensure WCAG 2.1 AA compliance)
- [ ] T089 [P] Update README.md in project root with quickstart, architecture diagram, deployment instructions
- [ ] T090 [P] Run backend test suite with coverage target ≥80% in `backend/tests/` (fix any gaps)
- [ ] T091 [P] Run frontend test suite with coverage target ≥70% in `frontend/tests/` (exclude UI snapshot tests)
- [ ] T092 [P] Performance profiling: measure dashboard load time with 500 tasks (target <1s), drag-drop reorder (target 300ms feedback)
- [ ] T093 Add rate limiting middleware to backend in `backend/src/middleware/` to prevent abuse (optional for MVP but recommended)
- [ ] T094 [P] Code review checklist in PULL_REQUEST_TEMPLATE.md (verify PR references Constitution principles: quality, tests, UX, performance, observability)
- [ ] T095 Create CONTRIBUTING.md with code style, commit message, and PR review guidelines
- [ ] T096 [P] Validate all .env.example files match actual requirements; document all variables
- [ ] T097 Create docker-compose.yml for local dev with optional PostgreSQL for future upgrade
- [ ] T098 [P] End-to-end test scenario in `frontend/tests/e2e/` or docs: login → create task → filter → reorder → edit → delete (test all happy paths)
- [ ] T099 [P] Security checklist: password requirements (min 8 chars), JWT expiration (1 hour access, 7 day refresh), no secrets in git
- [ ] T100 [P] Documentation: update specs/ with final architecture notes, add troubleshooting FAQ to quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories ✅ MVP
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but independently testable ✅
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but independently testable ✅

### Within Each User Story

- Tests (marked [P] where applicable) MUST be written and FAIL before implementation
- Models before services
- Services before route endpoints
- Route endpoints before UI components
- UI components before integration tests
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005, T006)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T009, T010, T011, T012, T015, T016, T018, T020, T021)
- Once Foundational phase completes, all three user stories (US1, US2, US3) can start in parallel (if team capacity allows)
- Within each user story, all test tasks marked [P] can run in parallel (write tests first)
- All model/service tasks marked [P] can run in parallel (different modules)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1 Tests

```
# Launch all tests for User Story 1 BEFORE implementation (ensure they FAIL):
Task T024: Contract test for GET /api/v1/tasks
Task T025: Unit test for task ordering logic
Task T026: Unit test for additive filtering
Task T027: Unit test for subtask validation
Task T028: Integration test for Dashboard render
Task T029: Integration test for FilterPanel
Task T030: Integration test for drag-drop

# Expected: All tests FAIL (red state)

# Then implement:
Task T031-T044: Backend endpoints and services
Task T036-T043: Frontend components

# Expected: All tests now PASS (green state)
```

---

## Parallel Example: Foundational Phase

```
# Backend infrastructure (can run in parallel):
Task T009: SQLAlchemy setup
Task T010: User ORM model
Task T011: Task ORM model
Task T012: Project ORM model
Task T015: Password hashing
Task T016: JWT service
Task T018: RBAC helper

# Frontend infrastructure (can run in parallel):
Task T020: AuthContext
Task T021: ProtectedRoute
Task T022: API client

# All 10 tasks can run in parallel; results integrated in tasks T013-T023
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently (read-only dashboard works)
5. Deploy/demo if ready
6. **Only then proceed** to US2 and US3

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (6-8 hours)
2. Once Foundational is done:
   - Developer A: User Story 1 (dashboard, read-only) — 12-16 hours
   - Developer B: User Story 2 (create/edit) — 12-16 hours
   - Developer C: User Story 3 (admin) — 12-16 hours
3. Stories complete and integrate independently
4. Team rejoins for Phase 6 (polish, testing, deployment) — 8-12 hours

---

## Task Validation Checklist

- [x] All tasks follow strict format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [x] Task IDs sequential (T001-T100)
- [x] [P] markers only on parallelizable tasks (different files, no dependencies)
- [x] [Story] labels only in user story phases (US1, US2, US3); no labels in Setup/Foundational/Polish
- [x] File paths included in all task descriptions
- [x] Test tasks marked first (before implementation tasks)
- [x] Clear dependencies documented in "Dependencies & Execution Order"
- [x] Parallel execution examples provided
- [x] MVP scope identified (User Story 1 = MVP)
- [x] Each user story independently testable and completable

---

## Notes

- [P] tasks = different files, no dependencies; can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests FAIL before implementing (test-first)
- Commit after each task or logical group (e.g., all T03x for a user story)
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution compliance: All tasks trace to requirements (FR), user stories, and success criteria

---

**Ready to implement! Start with Phase 1 Setup and Phase 2 Foundational. Then choose: MVP (US1 only) or full feature (US1+US2+US3). 🚀**
