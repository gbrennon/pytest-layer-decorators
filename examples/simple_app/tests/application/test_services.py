"""Application-layer tests — may import from domain and application only."""

import pytest
from pytest_layer_decorators import application

from simple_app.application.services import UserService
from simple_app.domain.models import User


class FakeRepository:
    """A lightweight fake for testing — lives in the test, not in infrastructure."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def find_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def list_all(self) -> list[User]:
        return list(self._users.values())


@application
class TestApplicationServices:
    def test_register_user(self) -> None:
        repo = FakeRepository()
        service = UserService(repo)

        user = service.register("Alice", "alice@example.com")
        assert user.name == "Alice"
        assert repo.find_by_id(user.id) is not None

    def test_register_invalid_user_raises(self) -> None:
        service = UserService(FakeRepository())
        with pytest.raises(ValueError, match="name must not be empty"):
            service.register("   ", "x@y.com")

    def test_list_users(self) -> None:
        service = UserService(FakeRepository())
        service.register("Alice", "a@b.com")
        service.register("Bob", "b@c.com")
        assert len(service.list_users()) == 2
