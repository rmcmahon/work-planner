# Feature Specification: Team Task Manager

**Feature Branch**: `001-team-task-manager`  
**Created**: 2026-01-09  
**Status**: Draft  
**Input**: User description: "Build an application that helps me manage my team and their tasks at work. Tasks have a name, description, priority, owner, project, delivery date, status (blocked, not blocked, in progress). For the initial app, just basic login with username and password with one provisioned admin user with the user name \"admin\" and password \"p@ssw0rd!\". The landing page should be the tasks dashboard, which shows the tasks in a priortised order from top to bottom. Tasks can be repriortised by moving them up and down the list, and tasks can be dropped on top of other tasks, which sets them as sub tasks. On the left of the page are the filters, where we can set values to filter tasks, such by owner, priority, status, target date, project and those filters are additive. There are three types of roles, viewer, worker and admin. Anyone can log in as a viewer, workers can create new tasks, edit existing tasks that are assigned to them, admins can do everything to all tasks as well as being the only users that can view the admin page which includes roles assignment to users, creating users and any other settings for the app."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dashboard (Priority: P1)

As any authenticated user I want to see a prioritized list of tasks on the landing page so I can quickly find the most important work.

**Why this priority**: The dashboard is the main workflow surface; delivering it first provides immediate value.

**Independent Test**: Log in as a viewer and verify the dashboard displays tasks ordered by priority and manual ordering preserved.

**Acceptance Scenarios**:

1. **Given** the user is authenticated, **When** they visit the app root, **Then** they see the tasks dashboard with tasks ordered by priority and manual position.
2. **Given** tasks exist with priorities and parent/child relationships, **When** a task is dropped onto another, **Then** it becomes a sub-task of the target and is displayed indented under the parent.
3. **Given** multiple filters are set on the left panel, **When** filters are applied, **Then** tasks shown satisfy all selected filter values (additive filters).


---

### User Story 2 - Create & Edit Tasks (Priority: P2)

As a worker (or admin) I want to create tasks and edit tasks assigned to me so I can track and update work.

**Why this priority**: Enables team members to add and update tasks, necessary for usage beyond read-only.

**Independent Test**: Log in as a worker, create a new task with required fields (name, priority, owner, project, delivery date, status). Edit an assigned task and verify changes persist and reflect on dashboard.

**Acceptance Scenarios**:

1. **Given** a user with role worker, **When** they create a task, **Then** the task appears on the dashboard with provided attributes.
2. **Given** a worker is assigned a task, **When** they edit the task, **Then** the edit is saved and visible to other users.

---

### User Story 3 - Role-Based Admin (Priority: P3)

As an admin I want to manage users and roles and access an admin page so I can govern the application and assign permissions.

**Why this priority**: Administrators control access and user lifecycle; required for multi-user environments.

**Independent Test**: Log in as the provisioned admin (`admin` / `p@ssw0rd!`), visit the admin page, create a new user, assign the `worker` role, and verify the new user can log in and create tasks.

**Acceptance Scenarios**:

1. **Given** the admin is authenticated, **When** they visit the admin page, **Then** they can create users and assign roles (`viewer`, `worker`, `admin`).
2. **Given** an admin assigns `worker` to a user, **When** that user logs in, **Then** they have create/edit permissions limited to their assigned tasks.

---

### Edge Cases

- Dropping a task onto itself or cycles: operations **MUST** be prevented and return a clear error.
- Concurrent reordering: if two users reorder simultaneously, last-write-wins or operational transform conflict resolution must be defined; initial implementation will use last-write-wins and a visible timestamp.
- Missing required fields: create/update operations **MUST** validate required fields and return actionable errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide user authentication with username and password.
- **FR-002**: System MUST provision a default admin user with username `admin` and password `p@ssw0rd!` on first run.
- **FR-003**: System MUST provide three roles: `viewer`, `worker`, `admin` with permission rules: viewers = read-only, workers = create tasks and edit tasks assigned to them, admins = full access including user management.
- **FR-004**: System MUST model tasks with fields: `name`, `description`, `priority` (e.g., low/medium/high or numeric), `owner` (user), `project` (string/id), `OKR` (Objective Key Results), `delivery_date` (date), `status` (blocked, not blocked, in progress), `parent_task` (nullable for subtasks), and `position` (for ordering within a list).
- **FR-005**: Tasks MUST be displayed on the dashboard in prioritized order (primary: priority, secondary: explicit manual ordering/position).
- **FR-006**: System MUST allow tasks to be reordered by drag-and-drop, including moving up/down and dropping onto another task to set `parent_task`.
- **FR-007**: System MUST provide left-panel additive filters: `owner`, `priority`, `status`, `delivery_date` (range or date), and `project`; filtered results are the intersection of selected filters.
- **FR-008**: System MUST enforce access control on all task operations according to role definitions.
- **FR-009**: System MUST expose an admin page accessible only to `admin` users for user and role management and application settings.
- **FR-010**: System MUST persist data so tasks and users survive restarts.

*Assumptions*: Authentication is username/password (no SSO). Initial implementation uses last-write-wins for concurrent edits. Priority values will be enumerable (Low/Medium/High) with ability to map to numeric ordering; persistence is via a simple relational store or file-backed DB (left unspecified here).

### Key Entities *(include if feature involves data)*

- **User**: id, username, password_hash, display_name, email (optional), role (`viewer|worker|admin`), created_at
- **Task**: id, name, description, priority, owner_id, project_id, delivery_date, status, parent_task_id, position, created_at, updated_at
- **Project**: id, name, optional metadata

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dashboard displays tasks ordered by priority and manual position; 95% of manual reorder operations succeed within 1 second and reflect for other users within 3 seconds under normal conditions.
- **SC-002**: Filtering reduces the visible task set to only tasks matching all selected filters; acceptance test must pass for owner, priority, status, delivery date, and project combinations.
- **SC-003**: Role enforcement correctness: 100% of access control tests pass for viewer/worker/admin scenarios (unit/integration tests).
- **SC-004**: Authentication works for the provisioned admin credentials out-of-the-box and admin can create a new user and assign roles.

### Non-functional

- The initial implementation MUST respond to dashboard load in under 1 second for up to 500 tasks in a dev/staging environment (profiling requirement; production targets TBD).

## Notes and Next Steps

- Deliver a minimal runnable prototype: simple backend (REST or similar) + minimal frontend (single page) demonstrating login, dashboard, drag/drop ordering, filters, task CRUD, and the admin page.
- Include automated unit tests for core task logic and integration tests for auth and permissions.

