import os
import textwrap

from pytest_layer_decorators._mock_check import load_mock_policy


class TestLoadMockPolicy:
    def test_defaults_with_no_config(self) -> None:
        """Without any config, domain+app allow mocks; infra+pres deny them."""
        policy = load_mock_policy(None)
        assert policy == {
            "domain": True,
            "application": True,
            "infrastructure": False,
            "presentation": False,
        }

    def test_pyproject_allow_mocks_overrides_defaults(self, tmp_path) -> None:
        tmp_path.joinpath("pyproject.toml").write_text(textwrap.dedent("""\
            [tool.pytest_layer_decorators.allow_mocks]
            infrastructure = true
            domain = false
        """))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            policy = load_mock_policy(None)
            assert policy == {
                "domain": False,
                "application": True,
                "infrastructure": True,
                "presentation": False,
            }
        finally:
            os.chdir(old_cwd)

    def test_pyproject_partial_override_leaves_other_defaults(self, tmp_path) -> None:
        tmp_path.joinpath("pyproject.toml").write_text(textwrap.dedent("""\
            [tool.pytest_layer_decorators.allow_mocks]
            presentation = true
        """))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            policy = load_mock_policy(None)
            assert policy == {
                "domain": True,
                "application": True,
                "infrastructure": False,
                "presentation": True,
            }
        finally:
            os.chdir(old_cwd)


class TestIniBool:
    def test_bool_value_returned_directly(self) -> None:
        from pytest_layer_decorators._mock_check import _ini_bool
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.getini.return_value = True
        assert _ini_bool(mock, "key") is True

        mock.getini.return_value = False
        assert _ini_bool(mock, "key") is False

    def test_string_true_values(self) -> None:
        from pytest_layer_decorators._mock_check import _ini_bool
        from unittest.mock import MagicMock

        mock = MagicMock()
        for val in ("true", "True", "TRUE", "1", "yes"):
            mock.getini.return_value = val
            assert _ini_bool(mock, "key") is True

    def test_string_false_values(self) -> None:
        from pytest_layer_decorators._mock_check import _ini_bool
        from unittest.mock import MagicMock

        mock = MagicMock()
        for val in ("false", "no", "0", "anything"):
            mock.getini.return_value = val
            assert _ini_bool(mock, "key") is False

    def test_list_value_uses_first_element(self) -> None:
        from pytest_layer_decorators._mock_check import _ini_bool
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.getini.return_value = ["true", "false"]
        assert _ini_bool(mock, "key") is True

        mock.getini.return_value = ["0"]
        assert _ini_bool(mock, "key") is False

    def test_getini_exception_returns_none(self) -> None:
        from pytest_layer_decorators._mock_check import _ini_bool
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.getini.side_effect = ValueError("boom")
        assert _ini_bool(mock, "key") is None

    def test_non_bool_non_string_non_list_returns_none(self) -> None:
        from pytest_layer_decorators._mock_check import _ini_bool
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.getini.return_value = 42
        assert _ini_bool(mock, "key") is None

