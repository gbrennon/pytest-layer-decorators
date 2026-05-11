import types

import pytest


def make_module_named(name: str, **attrs: object) -> types.ModuleType:
    mod = types.ModuleType(name)
    mod.__dict__.update(attrs)
    return mod


def make_test_module_with(imports: dict[str, types.ModuleType]) -> types.ModuleType:
    mod = types.ModuleType("tests.test_sample")
    mod.__dict__.update(imports)
    return mod


@pytest.fixture
def layer_patterns() -> dict[str, list[str]]:
    return {
        "domain": ["myapp.domain.*"],
        "application": ["myapp.application.*"],
        "infrastructure": ["myapp.infrastructure.*"],
        "presentation": ["myapp.presentation.*"],
    }
