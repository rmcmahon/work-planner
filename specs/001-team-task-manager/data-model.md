# Data Model: Team Task Manager

**Phase**: Phase 1 (Design)  
**Date**: 2026-02-05  
**Purpose**: Define entities, relationships, validation rules, and state transitions.

---

## Entity Diagram

```
User (1) ──┬─── (M) Task (owner_id)
           └─── (M) TaskAudit (user_id)

Task (1) ──┬─── (M) Task (parent_task_id)
           └─── (M) TaskAudit (task_id)

Project (1) ─── (M) Task (project_id)
```

---

## Entity Definitions

### User

Represents an application user with role-based permissions.

**Fields**:

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| `id` | UUID/Int | PK | Unique identifier |
| `username` | String(100) | UNIQUE, NOT NULL | Login identifier; case-insensitive comparison |
| `password_hash` | String(255) | NOT NULL | bcrypt hash (never plain text) |
| `display_name` | String(255) | NOT NULL | Full name or display name |
| `email` | String(255) | UNIQUE, NULL | Optional email; validated format |
| `role` | Enum | NOT NULL | Enum: `VIEWER`, `WORKER`, `ADMIN` |
| `created_at` | DateTime | NOT NULL, DEFAULT=now | UTC timestamp |
| `updated_at` | DateTime | NOT NULL, DEFAULT=now, AUTO_UPDATE | UTC timestamp |
| `is_active` | Boolean | NOT NULL, DEFAULT=true | Soft-delete flag; inactive users can't log in |

**Validation Rules**:

- `username`: 3–50 chars; alphanumeric + underscore only.
- `password`: minimum 8 chars (enforced on create/reset, not stored).
- `display_name`: non-empty; max 255 chars.
- `email`: optional; if provided, must be valid email format; case-insensitive storage.
- `role`: must be one of `VIEWER`, `WORKER`, `ADMIN`; no custom roles in MVP.

**Relationships**:

- User.id → Task.owner_id (one user owns many tasks).
- User.id → TaskAudit.user_id (one user creates/edits many audit entries).

**Seed Data**:

```python
User(
    username='admin',
    password_hash=bcrypt('p@ssw0rd!'),
    display_name='Administrator',
    email='admin@local',
    role=Role.ADMIN,
    is_active=True
)
```

---

### Project

Represents a logical grouping of tasks (e.g., "Q1 Initiative", "Mobile App Redesign").

**Fields**:

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| `id` | UUID/Int | PK | Unique identifier |
| `name` | String(255) | NOT NULL, UNIQUE | Project name |
| `description` | Text | NULL | Optional description |
| `metadata` | JSON | NULL | Key-value store for future extensibility |
| `created_at` | DateTime | NOT NULL, DEFAULT=now | UTC timestamp |
| `updated_at` | DateTime | NOT NULL, DEFAULT=now, AUTO_UPDATE | UTC timestamp |

**Validation Rules**:

- `name`: 1–255 chars; must be unique.
- `description`: optional; max 2000 chars.
- `metadata`: JSON object; no schema validation in MVP.

**Relationships**:

- Project.id → Task.project_id (one project has many tasks).

---

### Task

Represents a work item with priority, ownership, and status.

**Fields**:

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| `id` | UUID/Int | PK | Unique identifier |
| `name` | String(255) | NOT NULL | Task title |
| `description` | Text | NULL | Detailed task description |
| `priority` | Enum | NOT NULL, DEFAULT=MEDIUM | Enum: `LOW`, `MEDIUM`, `HIGH` |
| `owner_id` | UUID/Int | NOT NULL, FK | References User.id; task owner |
| `project_id` | UUID/Int | NULL, FK | References Project.id |
| `delivery_date` | Date | NULL | Target completion date |
| `status` | Enum | NOT NULL, DEFAULT=NOT_BLOCKED | Enum: `BLOCKED`, `NOT_BLOCKED`, `IN_PROGRESS` |
| `parent_task_id` | UUID/Int | NULL, FK | References Task.id (self-join for subtasks) |
| `position` | Float/Int | NOT NULL, DEFAULT=0 | Explicit ordering within siblings; allows fractional values for insertions between tasks |
| `created_at` | DateTime | NOT NULL, DEFAULT=now | UTC timestamp |
| `updated_at` | DateTime | NOT NULL, DEFAULT=now, AUTO_UPDATE | UTC timestamp |
| `created_by` | UUID/Int | NOT NULL, FK | User who created task; immutable after creation |
| `is_deleted` | Boolean | NOT NULL, DEFAULT=false | Soft-delete flag |

**Validation Rules**:

- `name`: 1–255 chars; cannot be empty.
- `description`: optional; max 5000 chars.
- `priority`: must be one of `LOW`, `MEDIUM`, `HIGH`.
- `owner_id`: must reference existing user; cannot be null.
- `project_id`: optional; if provided, must reference existing project.
- `delivery_date`: optional; if provided, must be >= today (no past dates).
- `status`: must be one of `BLOCKED`, `NOT_BLOCKED`, `IN_PROGRESS`.
- `parent_task_id`: optional; if provided, cannot be self-referential (task.id != parent_task_id); cannot create cycles (task A → B → C → A).
- `position`: float allowing fractional values (e.g., 1.5 inserted between 1 and 2).

**Ordering Rules**:

1. **Primary**: Tasks ordered by priority: `HIGH > MEDIUM > LOW` (numeric: 3 > 2 > 1).
2. **Secondary**: Within same priority, ordered by `position` field (ascending).
3. **Subtasks**: Displayed indented under parent; inherit parent priority for ordering within the parent's list.

**Access Control**:

- **VIEWER**: Can view tasks; cannot create, edit, or delete.
- **WORKER**: Can view all tasks; can create tasks (as owner); can edit tasks owned by self; cannot delete or change owner.
- **ADMIN**: Can view, create, edit, delete any task; can change owner.

**Soft Delete Behavior**:

- `is_deleted=true` hides task from normal queries.
- Admin can permanently delete or restore soft-deleted tasks.
- Deleting parent task does not delete subtasks; subtasks become independent (parent_task_id set to NULL).

**Relationships**:

- Task.owner_id → User.id (many tasks owned by one user).
- Task.project_id → Project.id (many tasks in one project).
- Task.parent_task_id → Task.id (self-join: one task has many subtasks).
- Task.created_by → User.id (immutable; tracks who created).

---

### TaskAudit (Optional for MVP, Include for Observability)

Represents a changelog of task modifications for audit trails and observability.

**Fields**:

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| `id` | UUID/Int | PK | Unique identifier |
| `task_id` | UUID/Int | NOT NULL, FK | References Task.id |
| `user_id` | UUID/Int | NOT NULL, FK | User who made the change |
| `action` | Enum | NOT NULL | Enum: `CREATE`, `UPDATE`, `DELETE`, `REORDER` |
| `field_changed` | String(100) | NULL | Which field was modified (e.g., "priority", "position") |
| `old_value` | Text | NULL | Previous value (JSON serialized if complex) |
| `new_value` | Text | NULL | New value (JSON serialized if complex) |
| `timestamp` | DateTime | NOT NULL, DEFAULT=now | UTC timestamp of change |

**Rationale**:

- Enables debugging concurrent edits (detect collisions, replay events).
- Observability: log who changed what and when.
- Potential future feature: undo/history UI.

**Access Control**:

- VIEWER, WORKER: Can view their own actions on tasks they can access.
- ADMIN: Can view all audit entries.

---

## Database Schema (SQL Pseudocode)

```sql
CREATE TABLE "user" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('VIEWER', 'WORKER', 'ADMIN')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "project" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NULL,
    metadata TEXT NULL, -- JSON
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "task" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'MEDIUM' CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
    owner_id INTEGER NOT NULL,
    project_id INTEGER NULL,
    delivery_date DATE NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'NOT_BLOCKED' CHECK (status IN ('BLOCKED', 'NOT_BLOCKED', 'IN_PROGRESS')),
    parent_task_id INTEGER NULL,
    position REAL NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (owner_id) REFERENCES "user"(id),
    FOREIGN KEY (project_id) REFERENCES "project"(id),
    FOREIGN KEY (parent_task_id) REFERENCES "task"(id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    CHECK (parent_task_id != id) -- Prevent self-referential parent
);

CREATE INDEX idx_task_owner ON "task"(owner_id);
CREATE INDEX idx_task_project ON "task"(project_id);
CREATE INDEX idx_task_priority ON "task"(priority);
CREATE INDEX idx_task_status ON "task"(status);
CREATE INDEX idx_task_delivery_date ON "task"(delivery_date);
CREATE INDEX idx_task_parent ON "task"(parent_task_id);
CREATE INDEX idx_task_deleted ON "task"(is_deleted);

CREATE TABLE "task_audit" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('CREATE', 'UPDATE', 'DELETE', 'REORDER')),
    field_changed VARCHAR(100) NULL,
    old_value TEXT NULL,
    new_value TEXT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES "task"(id),
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE INDEX idx_audit_task ON "task_audit"(task_id);
CREATE INDEX idx_audit_user ON "task_audit"(user_id);
CREATE INDEX idx_audit_timestamp ON "task_audit"(timestamp);
```

---

## State Transitions & Business Logic

### Task Lifecycle

```
CREATE → NOT_BLOCKED
  ↓
(WORKER/ADMIN)
  ├── EDIT → NOT_BLOCKED (priority, owner, dates, description)
  ├── MARK_BLOCKED → BLOCKED (status change)
  ├── MARK_IN_PROGRESS → IN_PROGRESS (status change)
  ├── MARK_NOT_BLOCKED → NOT_BLOCKED (status change)
  ├── REORDER → (position change, no status change)
  ├── MAKE_SUBTASK → (parent_task_id change)
  └── DELETE (soft) → is_deleted=true (ADMIN only)
```

**Valid Transitions**:
- Any status → any other status (no restrictions in MVP).
- Any task can become a subtask (assign parent_task_id), but not to itself or create cycles.
- Reordering (position change) is independent of status.

### Cycle Prevention for Subtasks

If `task_a.parent_task_id = task_b.id`, ensure `task_b.parent_task_id ≠ task_a.id` and no transitive cycles exist.

**Algorithm** (before saving parent_task_id change):
```
fn can_set_parent(task_id, proposed_parent_id):
    if task_id == proposed_parent_id:
        return False  # Can't be own parent
    
    ancestors = []
    current = task_db.get(proposed_parent_id)
    while current.parent_task_id is not None:
        ancestors.append(current.parent_task_id)
        if current.parent_task_id == task_id:
            return False  # Cycle detected
        current = task_db.get(current.parent_task_id)
    
    return True  # Safe to set parent
```

---

## Filtering & Query Patterns

### Additive Filters

When multiple filters are applied, results are the **intersection** (AND logic):

```
GET /api/v1/tasks?owner=2&priority=HIGH&status=IN_PROGRESS&project=5&delivery_date_from=2026-02-01&delivery_date_to=2026-02-28

Results: Tasks WHERE owner_id=2 AND priority='HIGH' AND status='IN_PROGRESS' AND project_id=5 AND delivery_date BETWEEN '2026-02-01' AND '2026-02-28' AND is_deleted=false
```

**Performance**: Indexes on each filtered column ensure fast queries.

### Dashboard View Query

```sql
SELECT *
FROM task
WHERE is_deleted = false
  AND (filter conditions)
ORDER BY priority DESC, position ASC
```

---

## Summary

**Key Design Decisions**:

1. **Soft Delete**: Tasks not permanently removed; enables audit trails and undo.
2. **Self-Join for Subtasks**: Flexible hierarchy; supports arbitrary nesting.
3. **Position Field**: Float allows insertions without cascading updates.
4. **Role-Based Access**: Each operation checks user role before execution.
5. **Audit Trail**: Optional but recommended for production observability.
6. **Cycle Prevention**: Client-side validation + DB constraints prevent invalid hierarchies.

**Next Step**: Generate API contracts (OpenAPI spec) and quickstart guide.
