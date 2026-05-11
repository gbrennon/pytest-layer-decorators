from pytest_layer_decorators._decorators import (
    application,
    domain,
    infrastructure,
    presentation,
)


class TestDecoratorsApplyMarkers:
    def test_domain_adds_marker(self) -> None:
        @domain
        def sample() -> None: ...
        names = {m.name for m in getattr(sample, "pytestmark", [])}
        assert "domain" in names

    def test_application_adds_marker(self) -> None:
        @application
        def sample() -> None: ...
        names = {m.name for m in getattr(sample, "pytestmark", [])}
        assert "application" in names

    def test_infrastructure_adds_marker(self) -> None:
        @infrastructure
        def sample() -> None: ...
        names = {m.name for m in getattr(sample, "pytestmark", [])}
        assert "infrastructure" in names

    def test_presentation_adds_marker(self) -> None:
        @presentation
        def sample() -> None: ...
        names = {m.name for m in getattr(sample, "pytestmark", [])}
        assert "presentation" in names

    def test_preserves_function_identity(self) -> None:
        @domain
        def my_test() -> int:
            return 42
        assert my_test() == 42
        assert my_test.__name__ == "my_test"
