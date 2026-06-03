"""Unit tests for plugin message-formatting helpers and module coverage."""

import importlib

from pytest_layer_decorators._plugin import (
    format_mock_violation_message,
    format_violation_message,
    summarize_allowed_layers,
)


class TestPluginModuleCoverage:
    """Reload _plugin to ensure module-level code is tracked by coverage."""

    def test_reload_plugin_for_module_coverage(self) -> None:
        import pytest_layer_decorators._plugin as pmod

        importlib.reload(pmod)
        # Basic sanity — the module still has its hooks
        assert hasattr(pmod, "pytest_addoption")
        assert hasattr(pmod, "pytest_runtest_setup")
        assert hasattr(pmod, "format_violation_message")
        assert hasattr(pmod, "summarize_allowed_layers")

    def test_resolve_test_module_from_item_no_parent(self) -> None:
        """Exercise the fallback path where item has no parent chain."""
        from unittest.mock import MagicMock

        from pytest_layer_decorators._plugin import resolve_test_module_from_item

        # Mock an item with no 'parent' but with a 'nodeid'
        fake_item = MagicMock()
        fake_item.nodeid = "fake_module.py::test_thing"
        # Remove 'parent' so it defaults to None-ish
        del fake_item.parent

        result = resolve_test_module_from_item(fake_item)
        # We don't have 'fake_module' in sys.modules, so result should be None
        assert result is None

    def test_resolve_test_module_from_item_nodeid_no_module(self) -> None:
        """Exercise the path where module is not in sys.modules."""
        from unittest.mock import MagicMock

        from pytest_layer_decorators._plugin import resolve_test_module_from_item

        fake_item = MagicMock()
        fake_item.nodeid = "nonexistent_module.py::test_thing"
        del fake_item.parent

        result = resolve_test_module_from_item(fake_item)
        assert result is None


class TestFormatViolationMessage:
    def test_formats_with_single_violation(self) -> None:
        msg = format_violation_message(
            "tests/test_x.py::test_something",
            "domain",
            ["  - 'myapp.infrastructure.db' (belongs to 'infrastructure' layer, not allowed from 'domain' layer)"],
        )
        assert "Layer violation" in msg
        assert "tests/test_x.py::test_something" in msg
        assert "@domain" in msg
        assert "myapp.infrastructure.db" in msg

    def test_formats_with_multiple_violations(self) -> None:
        msg = format_violation_message(
            "tests/test_x.py::test_bad",
            "domain",
            [
                "  - 'a' (belongs to 'infrastructure' layer)",
                "  - 'b' (belongs to 'presentation' layer)",
            ],
        )
        assert "Layer violation" in msg
        assert "a'" in msg
        assert "b'" in msg

    def test_includes_allowed_layers_summary(self) -> None:
        msg = format_violation_message(
            "t.py::test_x", "domain", ["  - violation"]
        )
        assert "nothing outside its own layer" in msg.lower()


class TestFormatMockViolationMessage:
    def test_formats_with_mock_evidence(self) -> None:
        msg = format_mock_violation_message(
            "tests/test_x.py::test_with_mock",
            "infrastructure",
            ["mock import 'Mock' (from unittest.mock)"],
        )
        assert "Mock violation" in msg
        assert "@infrastructure" in msg
        assert "mock import 'Mock'" in msg

    def test_formats_with_multiple_evidence_items(self) -> None:
        msg = format_mock_violation_message(
            "t.py::test_x",
            "presentation",
            ["mock object 'my_mock'", "mock import 'patch' (from unittest.mock)"],
        )
        assert "  - mock object 'my_mock'" in msg
        assert "  - mock import 'patch'" in msg


class TestSummarizeAllowedLayers:
    def test_empty_returns_nothing_outside_message(self) -> None:
        assert summarize_allowed_layers("domain") == "nothing outside its own layer"

    def test_non_empty_returns_comma_separated(self) -> None:
        assert summarize_allowed_layers("application") == "domain"
