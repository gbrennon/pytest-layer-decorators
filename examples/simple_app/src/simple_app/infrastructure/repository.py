"""Infrastructure layer — implements the repository port with in-memory storage."""

from simple_app.domain.models import User


class InMemoryUserRepository:
    """An in-memory adapter implementing the UserRepository port."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def find_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def list_all(self) -> list[User]:
        return list(self._users.values())
