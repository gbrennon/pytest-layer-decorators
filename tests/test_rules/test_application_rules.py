from pytest_layer_decorators._rules import check_layer_rules

from .helpers import layer_patterns, make_module_named, make_test_module_with


class TestApplicationLayerRules:
    def test_importing_domain_passes(self, layer_patterns) -> None:
        domain_mod = make_module_named("myapp.domain.models")
        test_mod = make_test_module_with({"Entity": domain_mod})
        assert check_layer_rules(test_mod, "application", layer_patterns) == []

    def test_importing_infrastructure_violates(self, layer_patterns) -> None:
        infra_mod = make_module_named("myapp.infrastructure.db")
        test_mod = make_test_module_with({"Database": infra_mod})
        violations = check_layer_rules(test_mod, "application", layer_patterns)
        assert len(violations) == 1
        assert "infrastructure" in violations[0]

    def test_importing_presentation_violates(self, layer_patterns) -> None:
        pres_mod = make_module_named("myapp.presentation.api")
        test_mod = make_test_module_with({"Controller": pres_mod})
        violations = check_layer_rules(test_mod, "application", layer_patterns)
        assert len(violations) == 1
        assert "presentation" in violations[0]
