from .helpers import setup_fake_project


class TestValidLayerUsage:
    def test_domain_test_with_domain_import_passes(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_domain="""
            from pytest_layer_decorators import domain
            from fake_app.domain.models import DomainEntity

            @domain
            def test_entity():
                assert DomainEntity() is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)

    def test_application_test_with_domain_import_passes(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_app="""
            from pytest_layer_decorators import application
            from fake_app.domain.models import DomainEntity

            @application
            def test_usecase():
                assert DomainEntity() is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)

    def test_infrastructure_test_with_application_import_passes(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_infra="""
            from pytest_layer_decorators import infrastructure
            from fake_app.application.usecases import CreateUserUseCase

            @infrastructure
            def test_adapter():
                assert CreateUserUseCase() is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)

    def test_presentation_test_with_application_import_passes(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_pres="""
            from pytest_layer_decorators import presentation
            from fake_app.application.usecases import CreateUserUseCase

            @presentation
            def test_controller():
                assert CreateUserUseCase() is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)

    def test_unmarked_test_can_import_anything(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_any="""
            from fake_app.domain.models import DomainEntity
            from fake_app.infrastructure.db import Database

            def test_mixed():
                assert DomainEntity() is not None
                assert Database() is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)
