"""Infrastructure-layer tests — may import from domain, application, infrastructure.

NOT allowed: presentation layer imports.
"""

from pytest_layer_decorators import infrastructure

from simple_app.application.services import UserService
from simple_app.domain.models import User
from simple_app.infrastructure.repository import InMemoryUserRepository


@infrastructure
class TestInfrastructureRepository:
    def test_save_and_retrieve_user(self) -> None:
        repo = InMemoryUserRepository()
        user = User(name="Alice", email="alice@example.com")
        repo.save(user)

        found = repo.find_by_id(user.id)
        assert found is not None
        assert found.name == "Alice"

    def test_find_by_id_returns_none_for_missing(self) -> None:
        repo = InMemoryUserRepository()
        assert repo.find_by_id("nonexistent") is None

    def test_list_all_returns_all_users(self) -> None:
        repo = InMemoryUserRepository()
        repo.save(User(name="Alice", email="a@b.com"))
        repo.save(User(name="Bob", email="b@c.com"))
        assert len(repo.list_all()) == 2

    def test_repository_works_with_service(self) -> None:
        """Infrastructure test using the real repository with the application service."""
        repo = InMemoryUserRepository()
        service = UserService(repo)

        service.register("Charlie", "charlie@example.com")
        assert len(repo.list_all()) == 1
