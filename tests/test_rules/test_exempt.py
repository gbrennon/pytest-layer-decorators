import pytest

from pytest_layer_decorators._exempt import is_module_exempt


class TestIsModuleExempt:
    @pytest.mark.parametrize(
        "name",
        ["os", "sys", "typing", "collections", "pytest", "_pytest", "pluggy",
         "os.path", "typing.List", "pytest.mark", "pytest_layer_decorators"],
    )
    def test_stdlib_and_tooling_are_exempt(self, name: str) -> None:
        assert is_module_exempt(name) is True

    @pytest.mark.parametrize(
        "name",
        ["myapp", "django", "requests", "flask", "sqlalchemy"],
    )
    def test_non_stdlib_are_not_exempt(self, name: str) -> None:
        assert is_module_exempt(name) is False
