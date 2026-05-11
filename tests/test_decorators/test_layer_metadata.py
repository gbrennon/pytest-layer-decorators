from pytest_layer_decorators._decorators import (
    application,
    domain,
    infrastructure,
    presentation,
)


class TestLayerNameMetadata:
    def test_domain_has_layer_name_attr(self) -> None:
        assert getattr(domain, "__layer_name__", None) == "domain"

    def test_application_has_layer_name_attr(self) -> None:
        assert getattr(application, "__layer_name__", None) == "application"

    def test_infrastructure_has_layer_name_attr(self) -> None:
        assert getattr(infrastructure, "__layer_name__", None) == "infrastructure"

    def test_presentation_has_layer_name_attr(self) -> None:
        assert getattr(presentation, "__layer_name__", None) == "presentation"
