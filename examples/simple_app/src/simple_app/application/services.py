"""Application layer — use cases / services that orchestrate domain objects."""

from typing import Protocol

from simple_app.domain.models import User


class UserRepository(Protocol):
    """Port (interface) that the application layer expects infrastructure to implement."""

    def save(self, user: User) -> None: ...
    def find_by_id(self, user_id: str) -> User | None: ...
    def list_all(self) -> list[User]: ...


class UserService:
    """Application service — depends only on the domain and the repository port."""

    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    def register(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        user.validate()
        self._repo.save(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        return self._repo.find_by_id(user_id)

    def list_users(self) -> list[User]:
        return self._repo.list_all()
