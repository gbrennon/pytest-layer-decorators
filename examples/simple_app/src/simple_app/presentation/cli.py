"""Presentation layer — thin CLI handler that delegates to application services."""

from simple_app.application.services import UserService


def handle_register(service: UserService, name: str, email: str) -> str:
    """CLI handler for the 'register' command."""
    user = service.register(name, email)
    return f"Registered user {user.id} ({user.name} <{user.email}>)"


def handle_list(service: UserService) -> str:
    """CLI handler for the 'list' command."""
    users = service.list_users()
    if not users:
        return "No users registered."
    lines = [f"  {u.id}  {u.name} <{u.email}>" for u in users]
    return "Users:\n" + "\n".join(lines)
