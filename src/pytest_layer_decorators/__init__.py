"""pytest-layer-decorators — reusable decorators for layer-separated test suites.

Decorate individual test functions or whole test classes::

    from pytest_layer_decorators import domain, application, infrastructure, presentation

    @domain
    def test_pure_business_logic():
        ...

    @application
    class TestUseCases:
        def test_register_user(self):
            ...

    @infrastructure
    def test_database_adapter():
        ...

    @presentation
    class TestCLI:
        def test_handle_command(self):
            ...
"""

from pytest_layer_decorators._decorators import (
    application,
    domain,
    infrastructure,
    presentation,
)

__all__ = ["application", "domain", "infrastructure", "presentation"]
