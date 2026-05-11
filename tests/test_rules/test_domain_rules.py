import sys

from pytest_layer_decorators._rules import check_layer_rules

from .helpers import layer_patterns, make_module_named, make_test_module_with


class TestDomainLayerRules:
    def test_importing_domain_module_passes(self, layer_patterns) -> None:
        domain_mod = make_module_named("myapp.domain.models")
        test_mod = make_test_module_with({"Entity": domain_mod})
        assert check_layer_rules(test_mod, "domain", layer_patterns) == []

    def test_importing_application_violates(self, layer_patterns) -> None:
        app_mod = make_module_named("myapp.application.usecases")
        test_mod = make_test_module_with({"UseCase": app_mod})
        violations = check_layer_rules(test_mod, "domain", layer_patterns)
        assert len(violations) == 1
        assert "application" in violations[0]

    def test_importing_infrastructure_violates(self, layer_patterns) -> None:
        infra_mod = make_module_named("myapp.infrastructure.db")
        test_mod = make_test_module_with({"Database": infra_mod})
        violations = check_layer_rules(test_mod, "domain", layer_patterns)
        assert len(violations) == 1
        assert "infrastructure" in violations[0]

    def test_importing_presentation_violates(self, layer_patterns) -> None:
        pres_mod = make_module_named("myapp.presentation.api")
        test_mod = make_test_module_with({"Controller": pres_mod})
        violations = check_layer_rules(test_mod, "domain", layer_patterns)
        assert len(violations) == 1
        assert "presentation" in violations[0]

    def test_stdlib_imports_are_always_exempt(self, layer_patterns) -> None:
        test_mod = make_test_module_with({"os": sys.modules["os"]})
        assert check_layer_rules(test_mod, "domain", layer_patterns) == []
