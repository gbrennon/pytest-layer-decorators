import types

from pytest_layer_decorators._rules import check_layer_rules


class TestEmptyConfigYieldsNoViolations:
    def test_empty_dict_returns_empty_list(self) -> None:
        mod = types.ModuleType("tests.any")
        assert check_layer_rules(mod, "domain", {}) == []

    def test_any_import_is_allowed_without_config(self) -> None:
        infra = types.ModuleType("myapp.infrastructure.db")
        mod = types.ModuleType("tests.any")
        mod.Database = infra
        assert check_layer_rules(mod, "domain", {}) == []
