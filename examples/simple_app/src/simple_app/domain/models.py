"""Domain layer — pure business objects, no external dependencies."""

import uuid
from dataclasses import dataclass, field


@dataclass
class User:
    """A user entity — pure domain object."""

    name: str
    email: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("User name must not be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email address")
