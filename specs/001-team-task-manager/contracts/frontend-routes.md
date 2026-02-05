# Frontend Routes & Navigation Contract

**Date**: 2026-02-05  
**Purpose**: Define frontend routes, components, and navigation flows for the React SPA.

---

## Route Map

```
/                          → LoginPage (if not authenticated) or DashboardPage (if authenticated)
/login                     → LoginPage
/dashboard                 → DashboardPage (protected; requires authentication)
/task/:id                  → TaskDetailModal (within DashboardPage)
/task/new                  → TaskFormModal (create new)
/admin                     → AdminPage (protected; requires ADMIN role)
/admin/users               → AdminPage (default tab)
/admin/projects            → AdminPage (projects tab)
/settings                  → SettingsPage (generic settings; future expansion)
/logout                    → Clear auth token + redirect to /login
```

---

## Page Components

### LoginPage

**Route**: `/login`  
**Access**: Public (redirected to dashboard if already authenticated)

**Responsibility**:
- Display login form (username + password).
- Handle login request to `POST /api/v1/auth/login`.
- Store JWT access token and refresh token securely (access token in memory or localStorage; refresh token in HTTP-only cookie).
- Redirect to dashboard on success.
- Display error message on login failure.

**Props/State**:
- `username` (string): form input
- `password` (string): form input
- `isLoading` (boolean): disable form while submitting
- `error` (string): error message display

**User Interactions**:
- Enter username and password.
- Click "Login" button.
- On success: redirect to `/dashboard`.
- On error: display error message inline.

---

### DashboardPage

**Route**: `/dashboard`  
**Access**: Protected (requires authentication)

**Responsibility**:
- Fetch and display tasks from backend.
- Manage filter state (owner, priority, status, delivery date, project).
- Display TaskList component with drag-and-drop.
- Display FilterPanel component on the left.
- Display buttons/modals for creating and editing tasks.
- Real-time re-fetch on task changes (or optimistic updates).

**Props/State**:
- `tasks` (Task[]): current filtered task list
- `filters` (object): active filters { owner_id?, priority?, status?, delivery_date_from?, delivery_date_to?, project_id? }
- `selectedTask` (Task | null): currently selected task for detail/edit
- `isLoadingTasks` (boolean): show loading spinner
- `showTaskForm` (boolean): show create/edit task modal

**Components**:
- `FilterPanel`: Left sidebar with filter controls
- `TaskList`: Main area with draggable tasks
- `TaskCard`: Individual task row
- `TaskFormModal`: Modal for create/edit (lazy-loaded or conditionally rendered)

**User Interactions**:
- Apply filters: filters update; re-fetch tasks with query params.
- Click task: open detail view or edit modal.
- Drag task up/down: reorder within same priority group; call `PATCH /api/v1/tasks/:id/position`.
- Drop task on another: make subtask; call `POST /api/v1/tasks/:id/parent`.
- Create new task: click "New Task" button; open `TaskFormModal`.
- Edit task: click edit icon on task; open `TaskFormModal`.

---

### TaskFormModal

**Route**: `/dashboard` (modal overlay)  
**Access**: Protected

**Responsibility**:
- Display form for creating or editing a task.
- Validate required fields (name, owner, priority).
- Submit to `POST /api/v1/tasks` (create) or `PATCH /api/v1/tasks/:id` (edit).
- Close modal on success; show error message on failure.

**Props**:
- `task` (Task | null): if editing, the task object; if null, create new task
- `onClose` (): callback to close modal
- `onSuccess` (task: Task): callback after successful save

**Form Fields**:
- `name` (text): required, 1–255 chars
- `description` (textarea): optional, max 5000 chars
- `priority` (select): LOW, MEDIUM, HIGH (default: MEDIUM)
- `owner_id` (select): dropdown of users (default: current user for WORKER)
- `project_id` (select): dropdown of projects, nullable
- `delivery_date` (date picker): optional
- `status` (select): BLOCKED, NOT_BLOCKED, IN_PROGRESS (default: NOT_BLOCKED)

**Access Control**:
- WORKER: can only set owner to self.
- ADMIN: can set owner to any user.

---

### TaskList

**Route**: `/dashboard` (sub-component)  
**Access**: Protected

**Responsibility**:
- Render draggable list of tasks using `react-beautiful-dnd`.
- Display tasks sorted by priority (HIGH → MEDIUM → LOW), then by position.
- Display subtasks indented under parent.
- Support drag-and-drop within the list and onto other tasks.
- Emit reorder events to parent component.

**Props**:
- `tasks` (Task[]): array of tasks to display
- `onTaskDrop` (sourceId: number, targetId?: number, newPosition?: number): callback on reorder
- `onTaskSelect` (task: Task): callback when task clicked

**Rendering Logic**:
```
For each task in tasks (sorted by priority DESC, position ASC):
  If task.parent_task_id is null:
    Render TaskCard as top-level (Draggable)
    If task has subtasks:
      Render subtasks indented under parent (Draggable within Droppable)
```

**Keyboard Navigation** (for accessibility):
- Tab: navigate between tasks.
- Enter/Space: select task (open detail).
- Arrow Up/Down: focus previous/next task (no reorder via keyboard in MVP; focus only).

---

### TaskCard

**Route**: `/dashboard` (sub-component)  
**Access**: Protected

**Responsibility**:
- Render a single task row with name, priority badge, owner, delivery date, status.
- Display edit/delete/reorder icons (context-sensitive based on user role).
- Support drag-and-drop initiation.

**Props**:
- `task` (Task): task object
- `isDragging` (boolean): visual feedback from react-beautiful-dnd
- `onEdit` (task: Task): callback to open edit modal
- `onSelect` (task: Task): callback when clicked

**Rendered Fields**:
- Priority badge (color-coded: RED=HIGH, YELLOW=MEDIUM, GREEN=LOW)
- Task name (main text)
- Owner (avatar or name)
- Delivery date (formatted, e.g., "Feb 14")
- Status tag (BLOCKED=red, IN_PROGRESS=blue, NOT_BLOCKED=gray)
- Edit icon (pencil)
- Delete icon (trash, ADMIN only)

---

### FilterPanel

**Route**: `/dashboard` (sub-component)  
**Access**: Protected

**Responsibility**:
- Display filter controls on the left sidebar.
- Allow users to select filter values (owner, priority, status, delivery date, project).
- Emit filter changes to parent component (DashboardPage).
- Show "Clear Filters" button.

**Props**:
- `filters` (object): current filter state
- `onFilterChange` (newFilters: object): callback when filter changed
- `users` (User[]): dropdown options for owner filter
- `projects` (Project[]): dropdown options for project filter

**Filter Controls**:
- **Owner**: Dropdown (multi-select optional; MVP: single select)
- **Priority**: Checkboxes (LOW, MEDIUM, HIGH)
- **Status**: Checkboxes (BLOCKED, NOT_BLOCKED, IN_PROGRESS)
- **Delivery Date**: Date range picker (from/to)
- **Project**: Dropdown (single or multi-select)
- **Clear Filters**: Button to reset all filters

**User Interaction**:
- Select a filter value.
- On change: emit `onFilterChange` with updated filters.
- Parent (DashboardPage) refetches tasks with new query params.

---

### AdminPage

**Route**: `/admin`  
**Access**: Protected (requires ADMIN role)

**Responsibility**:
- Display admin interface with tabs for Users and Projects.
- Allow admin to create, update, deactivate users.
- Allow admin to create and manage projects.
- Display settings or configuration options.

**Tabs**:

#### Tab: Users

- Table of users (id, username, display_name, email, role, is_active).
- Buttons: Create User, Edit, Deactivate.
- Create User modal: form with username, password, display_name, email, role.
- Edit User modal: form to change role, display_name, email.

**Endpoints Called**:
- `GET /api/v1/admin/users`: fetch user list
- `POST /api/v1/admin/users`: create user
- `PATCH /api/v1/admin/users/:id`: update user
- `DELETE /api/v1/admin/users/:id`: deactivate user

#### Tab: Projects

- Table of projects (id, name, description, created_at).
- Buttons: Create Project.
- Create Project modal: form with name and description.

**Endpoints Called**:
- `GET /api/v1/admin/projects`: fetch project list
- `POST /api/v1/admin/projects`: create project

---

## Navigation & Auth Flow

### Initial Load

```
1. App.tsx mounted.
2. Check for access_token in memory/localStorage.
3. If token exists:
   a. Validate token (check expiration).
   b. If expired: call refresh endpoint to get new access_token.
   c. If valid: fetch user profile (implicit from token) and render protected routes.
4. If no token: redirect to /login.
```

### Login Flow

```
1. User visits / or /login.
2. LoginPage displays form.
3. User submits username + password.
4. POST /api/v1/auth/login is called.
5. On success:
   a. Store access_token (memory or localStorage).
   b. Refresh token stored in HTTP-only cookie (automatic by browser).
   c. Redirect to /dashboard.
6. On error: display error message; stay on /login.
```

### Protected Route Handling

```
1. User navigates to /dashboard or /admin.
2. ProtectedRoute component checks for access_token.
3. If missing or invalid:
   a. Redirect to /login.
4. If token valid but user lacks required role (e.g., /admin but role != ADMIN):
   a. Display 403 Forbidden message.
   b. Redirect to /dashboard.
```

### Logout Flow

```
1. User clicks "Logout" button (in top nav or menu).
2. Clear access_token from memory/localStorage.
3. Clear refresh_token cookie (browser automatic or explicit).
4. Redirect to /login.
```

---

## State Management Architecture

### Global State (AuthContext)

```javascript
{
  user: {
    id: number,
    username: string,
    role: 'VIEWER' | 'WORKER' | 'ADMIN',
    display_name: string
  },
  access_token: string,
  refresh_token: string,
  isAuthenticated: boolean,
  isLoading: boolean
}
```

### Local Component State (DashboardPage)

```javascript
{
  tasks: Task[],
  filters: {
    owner_id?: number,
    priority?: string,
    status?: string,
    delivery_date_from?: string,
    delivery_date_to?: string,
    project_id?: number
  },
  selectedTask?: Task,
  isLoadingTasks: boolean,
  showTaskForm: boolean,
  error?: string
}
```

---

## Accessibility Considerations

- **Keyboard Navigation**: All interactive elements (buttons, inputs, modals) accessible via Tab and Enter/Space.
- **ARIA Labels**: Forms use `<label>` elements; modals use `role="dialog"` and `aria-modal="true"`.
- **Color Contrast**: Priority badges, status tags, and text meet WCAG AA (4.5:1) minimum.
- **Focus Management**: Modal focus trapped; focus returned to trigger button on close.
- **Semantic HTML**: Use `<button>`, `<form>`, `<input type="...">` instead of `<div>` elements.

---

## Error Handling

### Network Errors

- Catch fetch/axios errors; display user-friendly message (e.g., "Failed to load tasks. Please try again.").
- Retry button offered where appropriate.

### Auth Errors (401 Unauthorized)

- If API returns 401: invalidate token, redirect to /login.
- User prompted to log in again.

### Permission Errors (403 Forbidden)

- Display message: "You don't have permission to perform this action."
- Offer redirect to /dashboard or /admin based on user role.

### Validation Errors (400 Bad Request)

- Display field-specific errors inline in forms (e.g., "Name is required").
- Show API error message as fallback.

---

## Summary

**Frontend is a SPA** with the following key pages and flows:
- LoginPage: simple login form, JWT token storage.
- DashboardPage: main task management dashboard with filters, drag-and-drop, and CRUD.
- AdminPage: admin panel for user and project management.
- Protected routes: require valid JWT token and check role-based access.
- State: global auth state via Context; local component state for UI.
- Accessibility: semantic HTML, keyboard nav, WCAG AA colors and contrast.

**Next Phase**: Generate quickstart.md with setup and running instructions.
