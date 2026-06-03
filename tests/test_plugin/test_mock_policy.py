from .helpers import setup_fake_project


class TestMockPolicyAllowsMocksByDefault:
    """domain + application default to allow mocks."""

    def test_domain_test_with_mock_passes_when_not_configured(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_domain="""
            from unittest.mock import Mock
            from pytest_layer_decorators import domain

            @domain
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)
    def test_application_test_with_mock_passes_by_default(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_app="""
            from unittest.mock import Mock
            from pytest_layer_decorators import application

            @application
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)


class TestMockPolicyBlocksMocksByDefault:
    """infrastructure + presentation default to deny mocks."""

    def test_infrastructure_test_with_mock_fails_by_default(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_infra="""
            from unittest.mock import Mock
            from pytest_layer_decorators import infrastructure

            @infrastructure
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*Mock violation*"])

    def test_presentation_test_with_mock_fails_by_default(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_pres="""
            from unittest.mock import Mock
            from pytest_layer_decorators import presentation

            @presentation
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*Mock violation*"])

    def test_infrastructure_test_with_magic_mock_fails_by_default(self, pytester) -> None:
        setup_fake_project(pytester)
        pytester.makepyfile(test_infra="""
            from unittest.mock import MagicMock
            from pytest_layer_decorators import infrastructure

            @infrastructure
            def test_with_magic_mock():
                m = MagicMock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)


class TestMockPolicyBlocksMocksWhenDisabled:
    def _disable_domain_mocks(self, pytester) -> None:
        pytester.makefile(
            ".ini",
            pytest="""
[pytest]
layer_domain_allow_mocks = false
""",
        )

    def test_domain_test_with_mock_fails_when_disabled(self, pytester) -> None:
        self._disable_domain_mocks(pytester)
        setup_fake_project(pytester)
        pytester.makepyfile(test_domain="""
            from unittest.mock import Mock
            from pytest_layer_decorators import domain

            @domain
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*Mock violation*"])

    def test_domain_test_with_magic_mock_fails_when_disabled(self, pytester) -> None:
        self._disable_domain_mocks(pytester)
        setup_fake_project(pytester)
        pytester.makepyfile(test_domain="""
            from unittest.mock import MagicMock
            from pytest_layer_decorators import domain

            @domain
            def test_with_magic_mock():
                m = MagicMock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)

    def test_domain_test_with_patch_fails_when_disabled(self, pytester) -> None:
        self._disable_domain_mocks(pytester)
        setup_fake_project(pytester)
        pytester.makepyfile(test_domain="""
            from unittest.mock import patch
            from pytest_layer_decorators import domain

            @domain
            def test_with_patch():
                with patch("os.getcwd"):
                    pass
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)

    def test_application_test_with_mock_still_allowed_when_only_domain_disabled(self, pytester) -> None:
        self._disable_domain_mocks(pytester)
        setup_fake_project(pytester)
        pytester.makepyfile(test_app="""
            from unittest.mock import Mock
            from pytest_layer_decorators import application

            @application
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)



class TestMockPolicyPyprojectOverrides:
    """pyproject.toml allow_mocks can enable/disable per layer."""

    def test_pyproject_enables_mocks_for_infrastructure(self, pytester) -> None:
        pytester.makefile(
            ".toml",
            pyproject="""\
[tool.pytest_layer_decorators]
domain_modules = ["fake_app.domain.*"]
application_modules = ["fake_app.application.*"]
infrastructure_modules = ["fake_app.infrastructure.*"]
presentation_modules = ["fake_app.presentation.*"]

[tool.pytest_layer_decorators.allow_mocks]
infrastructure = true
""",
        )
        pytester.mkdir("fake_app")
        pytester.mkdir("fake_app/infrastructure")
        pytester.makepyfile(**{
            "fake_app/__init__": "",
            "fake_app/infrastructure/__init__": "",
            "fake_app/infrastructure/db": "class Database:\\n    pass\\n",
        })
        pytester.makepyfile(test_infra="""
            from unittest.mock import Mock
            from pytest_layer_decorators import infrastructure

            @infrastructure
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)

    def test_pyproject_disables_mocks_for_domain(self, pytester) -> None:
        pytester.makefile(
            ".toml",
            pyproject="""\
[tool.pytest_layer_decorators]
domain_modules = ["fake_app.domain.*"]
application_modules = ["fake_app.application.*"]
infrastructure_modules = ["fake_app.infrastructure.*"]
presentation_modules = ["fake_app.presentation.*"]

[tool.pytest_layer_decorators.allow_mocks]
domain = false
""",
        )
        pytester.mkdir("fake_app")
        pytester.mkdir("fake_app/domain")
        pytester.makepyfile(**{
            "fake_app/__init__": "",
            "fake_app/domain/__init__": "",
            "fake_app/domain/models": "class DomainEntity:\\n    pass\\n",
        })
        pytester.makepyfile(test_domain="""
            from unittest.mock import Mock
            from pytest_layer_decorators import domain

            @domain
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*Mock violation*"])

    def test_pyproject_enables_mocks_for_presentation(self, pytester) -> None:
        pytester.makefile(
            ".toml",
            pyproject="""\
[tool.pytest_layer_decorators]
domain_modules = ["fake_app.domain.*"]
application_modules = ["fake_app.application.*"]
infrastructure_modules = ["fake_app.infrastructure.*"]
presentation_modules = ["fake_app.presentation.*"]

[tool.pytest_layer_decorators.allow_mocks]
presentation = true
""",
        )
        pytester.mkdir("fake_app")
        pytester.mkdir("fake_app/presentation")
        pytester.makepyfile(**{
            "fake_app/__init__": "",
            "fake_app/presentation/__init__": "",
            "fake_app/presentation/api": "class ApiController:\\n    pass\\n",
        })
        pytester.makepyfile(test_pres="""
            from unittest.mock import Mock
            from pytest_layer_decorators import presentation

            @presentation
            def test_with_mock():
                m = Mock()
                assert m is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)
