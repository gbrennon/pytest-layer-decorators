from pytest_layer_decorators._rules import check_layer_rules

from .helpers import layer_patterns, make_module_named, make_test_module_with


class TestPresentationLayerRules:
    def test_importing_domain_passes(self, layer_patterns) -> None:
        domain_mod = make_module_named("myapp.domain.models")
        test_mod = make_test_module_with({"Entity": domain_mod})
        assert check_layer_rules(test_mod, "presentation", layer_patterns) == []

    def test_importing_application_passes(self, layer_patterns) -> None:
        app_mod = make_module_named("myapp.application.usecases")
        test_mod = make_test_module_with({"UseCase": app_mod})
        assert check_layer_rules(test_mod, "presentation", layer_patterns) == []

    def test_importing_infrastructure_violates(self, layer_patterns) -> None:
        infra_mod = make_module_named("myapp.infrastructure.db")
        test_mod = make_test_module_with({"Database": infra_mod})
        violations = check_layer_rules(test_mod, "presentation", layer_patterns)
        assert len(violations) == 1
        assert "infrastructure" in violations[0]
