from .helpers import setup_fake_project


class TestLayerViolations:
    def test_domain_importing_application_is_caught(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_violation="""
            from pytest_layer_decorators import domain
            from fake_app.application.usecases import CreateUserUseCase

            @domain
            def test_bad():
                pass
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*belongs to 'application' layer*"])

    def test_domain_importing_infrastructure_is_caught(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_violation="""
            from pytest_layer_decorators import domain
            from fake_app.infrastructure.db import Database

            @domain
            def test_bad():
                pass
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*belongs to 'infrastructure' layer*"])

    def test_domain_importing_presentation_is_caught(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_violation="""
            from pytest_layer_decorators import domain
            from fake_app.presentation.api import ApiController

            @domain
            def test_bad():
                pass
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)

    def test_application_importing_infrastructure_is_caught(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_violation="""
            from pytest_layer_decorators import application
            from fake_app.infrastructure.db import Database

            @application
            def test_bad():
                pass
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)

    def test_presentation_importing_infrastructure_is_caught(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_violation="""
            from pytest_layer_decorators import presentation
            from fake_app.infrastructure.db import Database

            @presentation
            def test_bad():
                pass
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)
