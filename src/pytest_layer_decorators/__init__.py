"""pytest-layer-decorators — reusable decorators for layer-separated test suites.

Usage::

    from pytest_layer_decorators import domain, application, infrastructure, presentation

    @domain
    def test_pure_business_logic():
        ...

    @application
    def test_use_case():
        ...

    @infrastructure
    def test_database_adapter():
        ...

    @presentation
    def test_api_controller():
        ...
"""

from pytest_layer_decorators._decorators import (
    application,
    domain,
    infrastructure,
    presentation,
)

__all__ = ["application", "domain", "infrastructure", "presentation"]
