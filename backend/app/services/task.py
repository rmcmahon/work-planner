"""Task service for business logic"""
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models import Task, TaskPriority, TaskStatus, Project
from app.services import Permission


class TaskService:
    """Service for task operations"""

    @staticmethod
    def create_task(
        db: Session,
        name: str,
        owner_id: str,
        project_id: str,
        created_by: str,
        description: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        status: TaskStatus = TaskStatus.TODO,
        delivery_date: Optional[datetime] = None,
        parent_task_id: Optional[str] = None,
    ) -> Task:
        """Create a new task"""
        # Validate parent task if specified
        if parent_task_id:
            if not TaskService.validate_parent_task(db, owner_id, parent_task_id):
                raise ValueError("Invalid parent task")

        # Find next position for this priority
        last_task = (
            db.query(Task)
            .filter(
                and_(
                    Task.priority == priority,
                    Task.is_deleted == False,
                )
            )
            .order_by(Task.position.desc())
            .first()
        )
        next_position = (last_task.position + 1) if last_task else 0.0

        task = Task(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            priority=priority,
            owner_id=owner_id,
            project_id=project_id,
            delivery_date=delivery_date,
            status=status,
            parent_task_id=parent_task_id,
            position=next_position,
            created_by=created_by,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(db: Session, task_id: str) -> Optional[Task]:
        """Get task by ID (excluding soft-deleted)"""
        return db.query(Task).filter(
            and_(
                Task.id == task_id,
                Task.is_deleted == False,
            )
        ).first()

    @staticmethod
    def get_ordered_tasks(db: Session, exclude_deleted: bool = True) -> List[Task]:
        """Get all tasks ordered by priority DESC, then position ASC"""
        query = db.query(Task)
        if exclude_deleted:
            query = query.filter(Task.is_deleted == False)

        # Map priority to numeric value for ordering (HIGH=3, MEDIUM=2, LOW=1)
        priority_order = {
            TaskPriority.HIGH: 3,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 1,
        }

        tasks = query.all()
        # Sort by priority (DESC) then position (ASC)
        return sorted(
            tasks,
            key=lambda t: (-priority_order.get(t.priority, 0), t.position),
        )

    @staticmethod
    def filter_tasks(
        db: Session,
        filters: Dict[str, Any],
    ) -> List[Task]:
        """
        Filter tasks with additive AND logic.
        Supported filters: owner_id, priority, status, project_id, delivery_date_from, delivery_date_to
        """
        query = db.query(Task).filter(Task.is_deleted == False)

        # Apply filters
        if "owner_id" in filters and filters["owner_id"]:
            query = query.filter(Task.owner_id == filters["owner_id"])

        if "priority" in filters and filters["priority"]:
            query = query.filter(Task.priority == filters["priority"])

        if "status" in filters and filters["status"]:
            query = query.filter(Task.status == filters["status"])

        if "project_id" in filters and filters["project_id"]:
            query = query.filter(Task.project_id == filters["project_id"])

        if "delivery_date_from" in filters and filters["delivery_date_from"]:
            from_date = filters["delivery_date_from"]
            if isinstance(from_date, str):
                from_date = datetime.fromisoformat(from_date)
            query = query.filter(Task.delivery_date >= from_date)

        if "delivery_date_to" in filters and filters["delivery_date_to"]:
            to_date = filters["delivery_date_to"]
            if isinstance(to_date, str):
                to_date = datetime.fromisoformat(to_date)
            # Include entire day by adding 1 day
            to_date_end = datetime.combine(to_date.date(), datetime.max.time())
            query = query.filter(Task.delivery_date <= to_date_end)

        # Order results
        tasks = query.all()
        return TaskService._apply_ordering(tasks)

    @staticmethod
    def _apply_ordering(tasks: List[Task]) -> List[Task]:
        """Apply priority DESC, position ASC ordering"""
        priority_order = {
            TaskPriority.HIGH: 3,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 1,
        }
        return sorted(
            tasks,
            key=lambda t: (-priority_order.get(t.priority, 0), t.position),
        )

    @staticmethod
    def validate_parent_task(db: Session, parent_task_id: str, task_id: str) -> bool:
        """
        Validate parent-child relationship.
        Returns False if:
        - task_id is same as parent_task_id (self-parent)
        - would create circular relationship
        """
        # Check self-parent
        if parent_task_id == task_id:
            return False

        # Check circular relationship: parent cannot be a descendant of this task
        current = db.query(Task).filter(Task.id == parent_task_id).first()
        while current:
            if current.parent_task_id == task_id:
                return False
            current = (
                db.query(Task)
                .filter(Task.id == current.parent_task_id)
                .first()
            )

        return True

    @staticmethod
    def reorder_task(
        db: Session,
        task_id: str,
        new_position: float,
        new_parent_id: Optional[str] = None,
    ) -> Task:
        """Reorder task and optionally change parent"""
        task = TaskService.get_task_by_id(db, task_id)
        if not task:
            raise ValueError("Task not found")

        # Validate new parent if specified
        if new_parent_id and not TaskService.validate_parent_task(db, new_parent_id, task_id):
            raise ValueError("Invalid parent task")

        task.position = new_position
        if new_parent_id is not None:
            task.parent_task_id = new_parent_id

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def update_task(db: Session, task_id: str, **kwargs) -> Optional[Task]:
        """Update task fields"""
        task = TaskService.get_task_by_id(db, task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if value is not None and hasattr(task, key):
                setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def soft_delete_task(db: Session, task_id: str) -> Optional[Task]:
        """Soft delete a task"""
        task = TaskService.get_task_by_id(db, task_id)
        if task:
            task.is_deleted = True
            db.commit()
            db.refresh(task)
        return task

    @staticmethod
    def get_task_subtasks(db: Session, task_id: str) -> List[Task]:
        """Get all subtasks of a task (recursively)"""
        direct_children = (
            db.query(Task)
            .filter(
                and_(
                    Task.parent_task_id == task_id,
                    Task.is_deleted == False,
                )
            )
            .all()
        )

        all_children = list(direct_children)
        for child in direct_children:
            all_children.extend(TaskService.get_task_subtasks(db, child.id))

        return all_children
