from pytest_layer_decorators._config import get_allowed_layers


class TestAllowedLayers:
    def test_domain_allows_nothing(self) -> None:
        assert get_allowed_layers("domain") == set()

    def test_application_allows_domain(self) -> None:
        assert get_allowed_layers("application") == {"domain"}

    def test_infrastructure_allows_domain_and_application(self) -> None:
        assert get_allowed_layers("infrastructure") == {"domain", "application"}

    def test_presentation_allows_domain_and_application(self) -> None:
        assert get_allowed_layers("presentation") == {"domain", "application"}

    def test_unknown_layer_returns_empty(self) -> None:
        assert get_allowed_layers("nonexistent") == set()
