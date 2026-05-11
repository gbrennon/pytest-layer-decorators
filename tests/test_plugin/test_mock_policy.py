from .helpers import setup_fake_project


class TestMockPolicyAllowsMocksByDefault:
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
