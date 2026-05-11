from pytest_layer_decorators._rules import check_layer_rules

from .helpers import layer_patterns, make_module_named, make_test_module_with


class TestTransitiveImportViolations:
    def test_detects_violation_through_transitive_module(self, layer_patterns) -> None:
        infra = make_module_named("myapp.infrastructure.db")
        app = make_module_named("myapp.application.usecases", Database=infra)
        test_mod = make_test_module_with({"UseCase": app})
        violations = check_layer_rules(test_mod, "application", layer_patterns)
        assert len(violations) == 1
        assert "infrastructure" in violations[0]
