"""Domain-layer tests — may only import from simple_app.domain.*"""

import pytest
from pytest_layer_decorators import domain

from simple_app.domain.models import User


@domain
class TestDomainModels:
    def test_user_creation(self) -> None:
        user = User(name="Alice", email="alice@example.com")
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.id  # auto-generated

    def test_user_validation_rejects_empty_name(self) -> None:
        user = User(name="   ", email="bob@example.com")
        with pytest.raises(ValueError, match="name must not be empty"):
            user.validate()

    def test_user_validation_rejects_invalid_email(self) -> None:
        user = User(name="Bob", email="not-an-email")
        with pytest.raises(ValueError, match="Invalid email"):
            user.validate()


# =====================================================================
# UNCOMMENT the test below to see a layer violation in action.
# A @domain test must NOT import from application, infrastructure,
# or presentation layers.
# =====================================================================

# @domain
# class TestDomainViolation:
#     def test_violation_imports_infrastructure(self) -> None:
#         from simple_app.infrastructure.repository import InMemoryUserRepository
#         repo = InMemoryUserRepository()
#         assert repo is not None
