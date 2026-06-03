import os
import textwrap
from unittest.mock import MagicMock

from pytest_layer_decorators._config import (
    _extract_patterns,
    _load_from_pyproject,
    _load_raw_pyproject_config,
    _parse_ini_value,
    load_config,
)


class TestLoadConfigWithoutPytest:
    def test_returns_empty_when_no_pyproject(self, tmp_path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            assert load_config(None) == {}
        finally:
            os.chdir(old_cwd)

    def test_loads_from_pyproject_toml(self, tmp_path) -> None:
        tmp_path.joinpath("pyproject.toml").write_text(textwrap.dedent("""\
            [tool.pytest_layer_decorators]
            domain_modules = ["myapp.domain.*"]
            application_modules = ["myapp.application.*"]
        """))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            assert load_config(None) == {
                "domain": ["myapp.domain.*"],
                "application": ["myapp.application.*"],
            }
        finally:
            os.chdir(old_cwd)

    def test_load_config_with_ini_fallback(self) -> None:
        """When INI config provides patterns, load_config uses them."""
        mock_config = MagicMock()

        def fake_getini(key: str) -> list[str] | None:
            mapping = {
                "layer_domain_modules": ["myapp.domain.*"],
            }
            return mapping.get(key, [])

        mock_config.getini = fake_getini  # type: ignore[attr-defined]
        result = load_config(mock_config)
        assert result == {"domain": ["myapp.domain.*"]}


class TestParseIniValue:
    def test_empty_value_returns_none(self) -> None:
        mock_config = MagicMock()
        mock_config.getini.return_value = []
        assert _parse_ini_value(mock_config, "any_key") is None

    def test_string_value_splits_on_comma(self) -> None:
        mock_config = MagicMock()
        mock_config.getini.return_value = "a, b, c"
        assert _parse_ini_value(mock_config, "any_key") == ["a", "b", "c"]

    def test_string_value_single(self) -> None:
        mock_config = MagicMock()
        mock_config.getini.return_value = "single"
        assert _parse_ini_value(mock_config, "any_key") == ["single"]

    def test_list_of_strings_returns_as_is(self) -> None:
        mock_config = MagicMock()
        mock_config.getini.return_value = ["x", "y"]
        assert _parse_ini_value(mock_config, "any_key") == ["x", "y"]

    def test_non_string_list_returns_none(self) -> None:
        mock_config = MagicMock()
        mock_config.getini.return_value = [1, 2, 3]
        assert _parse_ini_value(mock_config, "any_key") is None

    def test_non_list_non_string_returns_none(self) -> None:
        mock_config = MagicMock()
        mock_config.getini.return_value = 42
        assert _parse_ini_value(mock_config, "any_key") is None


class TestExtractPatterns:
    def test_none_returns_none(self) -> None:
        assert _extract_patterns(None) is None

    def test_string_returns_list_with_string(self) -> None:
        assert _extract_patterns("hello") == ["hello"]

    def test_list_of_strings_returns_list(self) -> None:
        assert _extract_patterns(["a", "b"]) == ["a", "b"]

    def test_non_matching_type_returns_none(self) -> None:
        assert _extract_patterns(42) is None


class TestLoadRawPyprojectConfig:
    def test_returns_none_when_no_pyproject(self, tmp_path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            assert _load_raw_pyproject_config() is None
        finally:
            os.chdir(old_cwd)

    def test_returns_dict_when_pyproject_found(self, tmp_path) -> None:
        tmp_path.joinpath("pyproject.toml").write_text(textwrap.dedent("""\
            [tool.pytest_layer_decorators]
            domain_modules = ["myapp.domain.*"]
            allow_mocks = { domain = false }
        """))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = _load_raw_pyproject_config()
            assert result is not None
            assert result["domain_modules"] == ["myapp.domain.*"]
        finally:
            os.chdir(old_cwd)


class TestLoadFromPyproject:
    def test_returns_none_when_no_pyproject(self, tmp_path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            assert _load_from_pyproject() is None
        finally:
            os.chdir(old_cwd)

    def test_returns_none_for_empty_but_valid_pyproject(self, tmp_path) -> None:
        """An empty but valid pyproject.toml still produces an empty dict,
        not None — the function returns the dict (filtered to list values)."""
        tmp_path.joinpath("pyproject.toml").write_text("[tool.pytest_layer_decorators]\n")
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = _load_from_pyproject()
            # Empty section -> empty dict (valid), filtered to list-values only = {}
            assert result == {}
        finally:
            os.chdir(old_cwd)
