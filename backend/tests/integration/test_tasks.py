"""Tests for task endpoints"""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models import User, UserRole, Task, TaskPriority, TaskStatus, Project
from app.core.security import create_access_token
from app.services import AuthService


# Contract test for GET /api/v1/tasks (T024)
def test_get_tasks_endpoint_contract(client: TestClient, db: Session):
    """
    Contract test: Verify GET /api/v1/tasks endpoint returns correct response schema.
    This test should FAIL until endpoint is implemented.
    """
    # Create test user and token
    user = AuthService.create_user(
        db=db,
        username="testuser",
        email="test@test.local",
        password="password",
        role=UserRole.VIEWER,
    )
    
    token = create_access_token({"sub": user.id})
    
    # Create test project
    project = Project(
        id=str(uuid4()),
        name="Test Project",
        description="Test",
    )
    db.add(project)
    db.commit()
    
    # Create test tasks
    for i in range(3):
        task = Task(
            id=str(uuid4()),
            name=f"Task {i+1}",
            description=f"Test task {i+1}",
            priority=TaskPriority.HIGH,
            owner_id=user.id,
            project_id=project.id,
            status=TaskStatus.TODO,
            position=float(i),
            created_by=user.id,
        )
        db.add(task)
    db.commit()
    
    # Call endpoint with auth
    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    # Verify response structure
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert "tasks" in data, "Response should contain 'tasks' key"
    assert "total" in data, "Response should contain 'total' key"
    assert isinstance(data["tasks"], list), "tasks should be a list"
    assert isinstance(data["total"], int), "total should be an integer"
    
    # Verify task schema
    assert data["total"] == 3
    assert len(data["tasks"]) == 3
    
    for task in data["tasks"]:
        assert "id" in task
        assert "name" in task
        assert "priority" in task
        assert "owner_id" in task
        assert "project_id" in task
        assert "status" in task
        assert "position" in task


# Unit test for task ordering logic (T025)
def test_task_ordering_by_priority_then_position(db: Session):
    """
    Unit test: Verify tasks are ordered by priority DESC, then position ASC.
    This test should FAIL until ordering logic is implemented.
    """
    # Create test user and project
    user = AuthService.create_user(
        db=db,
        username="ordertest",
        email="order@test.local",
        password="pass",
        role=UserRole.WORKER,
    )
    
    project = Project(
        id=str(uuid4()),
        name="Order Test Project",
    )
    db.add(project)
    db.commit()
    
    # Create tasks with mixed priority and position
    tasks_data = [
        (TaskPriority.LOW, 3.0),
        (TaskPriority.HIGH, 2.0),
        (TaskPriority.HIGH, 1.0),
        (TaskPriority.MEDIUM, 1.0),
        (TaskPriority.HIGH, 3.0),
    ]
    
    for priority, position in tasks_data:
        task = Task(
            id=str(uuid4()),
            name=f"Task {priority}_{position}",
            priority=priority,
            owner_id=user.id,
            project_id=project.id,
            status=TaskStatus.TODO,
            position=position,
            created_by=user.id,
        )
        db.add(task)
    db.commit()
    
    # Import the ordering service (to be implemented in T032)
    from app.services.task import TaskService
    
    ordered_tasks = TaskService.get_ordered_tasks(db)
    
    # Verify ordering: HIGH (1.0, 2.0, 3.0), MEDIUM (1.0), LOW (3.0)
    expected_order = [
        (TaskPriority.HIGH, 1.0),
        (TaskPriority.HIGH, 2.0),
        (TaskPriority.HIGH, 3.0),
        (TaskPriority.MEDIUM, 1.0),
        (TaskPriority.LOW, 3.0),
    ]
    
    actual_order = [(t.priority, t.position) for t in ordered_tasks]
    assert actual_order == expected_order, f"Expected {expected_order}, got {actual_order}"


# Unit test for additive filtering (T026)
def test_task_filtering_additive(db: Session):
    """
    Unit test: Verify additive filtering (owner + priority + status + date + project).
    AND logic for all filters. This test should FAIL until filtering logic is implemented.
    """
    # Create test users and project
    owner1 = AuthService.create_user(
        db=db, username="owner1", email="owner1@test.local", password="pass", role=UserRole.WORKER
    )
    owner2 = AuthService.create_user(
        db=db, username="owner2", email="owner2@test.local", password="pass", role=UserRole.WORKER
    )
    
    project1 = Project(id=str(uuid4()), name="Project 1")
    project2 = Project(id=str(uuid4()), name="Project 2")
    db.add_all([project1, project2])
    db.commit()
    
    # Create tasks with various combinations
    delivery_today = datetime.utcnow().date()
    delivery_tomorrow = (datetime.utcnow() + timedelta(days=1)).date()
    
    tasks_data = [
        (owner1.id, project1.id, TaskPriority.HIGH, TaskStatus.TODO, delivery_today),
        (owner1.id, project1.id, TaskPriority.HIGH, TaskStatus.IN_PROGRESS, delivery_today),
        (owner1.id, project2.id, TaskPriority.HIGH, TaskStatus.TODO, delivery_today),
        (owner2.id, project1.id, TaskPriority.HIGH, TaskStatus.TODO, delivery_today),
        (owner1.id, project1.id, TaskPriority.MEDIUM, TaskStatus.TODO, delivery_tomorrow),
    ]
    
    for owner_id, project_id, priority, status, delivery in tasks_data:
        task = Task(
            id=str(uuid4()),
            name=f"Task {owner_id[:8]}_{priority}_{status}",
            priority=priority,
            owner_id=owner_id,
            project_id=project_id,
            status=status,
            delivery_date=datetime.combine(delivery, datetime.min.time()),
            position=0.0,
            created_by=owner_id,
        )
        db.add(task)
    db.commit()
    
    from app.services.task import TaskService
    
    # Test filter: owner1 + priority HIGH + status TODO + project1 + delivery_today
    filters = {
        "owner_id": owner1.id,
        "priority": TaskPriority.HIGH,
        "status": TaskStatus.TODO,
        "project_id": project1.id,
        "delivery_date_from": delivery_today,
        "delivery_date_to": delivery_today,
    }
    
    filtered = TaskService.filter_tasks(db, filters)
    
    # Should match exactly 1 task
    assert len(filtered) == 1
    assert filtered[0].owner_id == owner1.id
    assert filtered[0].priority == TaskPriority.HIGH
    assert filtered[0].status == TaskStatus.TODO
    assert filtered[0].project_id == project1.id


# Unit test for subtask validation (T027)
def test_subtask_no_cycles_or_self_parent(db: Session):
    """
    Unit test: Verify subtask hierarchy prevents cycles and self-parent.
    This test should FAIL until cycle detection logic is implemented.
    """
    user = AuthService.create_user(
        db=db, username="subtestuser", email="subtest@test.local", password="pass", role=UserRole.WORKER
    )
    project = Project(id=str(uuid4()), name="Subtask Test")
    db.add(project)
    db.commit()
    
    # Create parent task
    parent = Task(
        id=str(uuid4()),
        name="Parent",
        owner_id=user.id,
        project_id=project.id,
        status=TaskStatus.TODO,
        position=0.0,
        created_by=user.id,
    )
    db.add(parent)
    db.commit()
    
    from app.services.task import TaskService
    
    # Test 1: Self-parent should be invalid
    assert not TaskService.validate_parent_task(db, parent.id, parent.id), "Task cannot be its own parent"
    
    # Test 2: Create child task
    child = Task(
        id=str(uuid4()),
        name="Child",
        owner_id=user.id,
        project_id=project.id,
        parent_task_id=parent.id,
        status=TaskStatus.TODO,
        position=0.0,
        created_by=user.id,
    )
    db.add(child)
    db.commit()
    
    # Test 3: Circular parent should be invalid (child cannot be parent of parent)
    assert not TaskService.validate_parent_task(db, parent.id, child.id), "Circular parent relationship not allowed"


@pytest.mark.asyncio
async def test_unauthenticated_get_tasks_fails(client: TestClient):
    """Verify GET /api/v1/tasks requires authentication"""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 403, "Should require authentication"
