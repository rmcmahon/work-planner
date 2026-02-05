"""Authorization and permission checking utilities"""
from typing import List, Optional
from app.models import User, UserRole


class Permission:
    """Permission definitions and checking"""

    # Define permissions by role
    ROLE_PERMISSIONS = {
        UserRole.VIEWER: [
            "read_tasks",
            "read_projects",
        ],
        UserRole.WORKER: [
            "read_tasks",
            "read_projects",
            "create_task",
            "edit_own_task",
            "update_task_status",
            "reorder_tasks",
        ],
        UserRole.ADMIN: [
            "read_tasks",
            "read_projects",
            "create_task",
            "edit_own_task",
            "edit_any_task",
            "delete_task",
            "update_task_status",
            "reorder_tasks",
            "manage_users",
            "manage_projects",
            "view_audit_logs",
        ],
    }

    @staticmethod
    def has_permission(user: User, permission: str) -> bool:
        """Check if user has a specific permission"""
        if user.role not in Permission.ROLE_PERMISSIONS:
            return False
        return permission in Permission.ROLE_PERMISSIONS[user.role]

    @staticmethod
    def has_any_permission(user: User, permissions: List[str]) -> bool:
        """Check if user has any of the specified permissions"""
        return any(Permission.has_permission(user, perm) for perm in permissions)

    @staticmethod
    def has_all_permissions(user: User, permissions: List[str]) -> bool:
        """Check if user has all specified permissions"""
        return all(Permission.has_permission(user, perm) for perm in permissions)

    @staticmethod
    def can_edit_task(user: User, task_owner_id: str) -> bool:
        """Check if user can edit a task (own task or admin)"""
        if Permission.has_permission(user, "edit_any_task"):
            return True
        if Permission.has_permission(user, "edit_own_task") and user.id == task_owner_id:
            return True
        return False

    @staticmethod
    def can_delete_task(user: User) -> bool:
        """Check if user can delete a task (admin only)"""
        return Permission.has_permission(user, "delete_task")

    @staticmethod
    def can_manage_users(user: User) -> bool:
        """Check if user can manage users (admin only)"""
        return Permission.has_permission(user, "manage_users")

    @staticmethod
    def can_manage_projects(user: User) -> bool:
        """Check if user can manage projects (admin only)"""
        return Permission.has_permission(user, "manage_projects")


class AccessControl:
    """Access control enforcement"""

    @staticmethod
    def verify_user_active(user: Optional[User]) -> bool:
        """Verify user exists and is active"""
        return user is not None and user.is_active

    @staticmethod
    def verify_user_role(user: User, required_roles: List[UserRole]) -> bool:
        """Verify user has one of the required roles"""
        return user.role in required_roles
