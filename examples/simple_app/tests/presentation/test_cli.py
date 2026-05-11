"""Presentation-layer tests — may import from domain, application, presentation.

NOT allowed: infrastructure layer imports (should use fakes instead).
"""

from pytest_layer_decorators import presentation

from simple_app.application.services import UserService
from simple_app.domain.models import User
from simple_app.presentation.cli import handle_list, handle_register


class FakeRepository:
    """Fake used by presentation tests — no infrastructure import needed."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def find_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def list_all(self) -> list[User]:
        return list(self._users.values())


@presentation
class TestPresentationCLI:
    def test_handle_register_returns_confirmation(self) -> None:
        service = UserService(FakeRepository())
        result = handle_register(service, "Alice", "alice@example.com")
        assert "Registered user" in result
        assert "Alice" in result

    def test_handle_list_when_empty(self) -> None:
        service = UserService(FakeRepository())
        result = handle_list(service)
        assert "No users" in result

    def test_handle_list_with_users(self) -> None:
        service = UserService(FakeRepository())
        handle_register(service, "Alice", "a@b.com")
        handle_register(service, "Bob", "b@c.com")

        result = handle_list(service)
        assert "Alice" in result
        assert "Bob" in result
