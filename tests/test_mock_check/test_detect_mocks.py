import os as os_mod
from unittest.mock import MagicMock, Mock, patch

from pytest_layer_decorators._mock_check import detect_mocks_in_namespace

from .helpers import make_module_named


class TestDetectMocksInNamespace:
    def test_empty_module_returns_nothing(self) -> None:
        mod = make_module_named("tests.example")
        assert detect_mocks_in_namespace(mod) == []

    def test_detects_unittest_mock_import(self) -> None:
        import unittest.mock as mock_mod
        mod = make_module_named("tests.example", mock=mock_mod)
        result = detect_mocks_in_namespace(mod)
        assert any("unittest.mock" in item for item in result)

    def test_detects_mock_instance(self) -> None:
        mod = make_module_named("tests.example", my_mock=Mock())
        result = detect_mocks_in_namespace(mod)
        assert any("my_mock" in item for item in result)

    def test_detects_magic_mock_instance(self) -> None:
        mod = make_module_named("tests.example", my_mock=MagicMock())
        result = detect_mocks_in_namespace(mod)
        assert any("my_mock" in item for item in result)

    def test_detects_mock_class_reference(self) -> None:
        mod = make_module_named("tests.example", MockClass=Mock)
        result = detect_mocks_in_namespace(mod)
        assert any("MockClass" in item for item in result)

    def test_does_not_flag_regular_objects(self) -> None:
        mod = make_module_named("tests.example", value=42, text="hello")
        assert detect_mocks_in_namespace(mod) == []

    def test_detects_patch_import(self) -> None:
        mod = make_module_named("tests.example", patch=patch)
        result = detect_mocks_in_namespace(mod)
        assert any("patch" in item for item in result)

    def test_exempt_module_is_not_walked(self) -> None:
        """Modules matching stdlib/tooling prefixes are skipped entirely."""
        mod = make_module_named("tests.example", os=os_mod)
        result = detect_mocks_in_namespace(mod)
        # 'os' itself is exempt, so neither 'os' nor its children are flagged
        assert not any("os" in item for item in result)

    def test_recurses_into_non_exempt_submodules(self) -> None:
        """Non-exempt submodules are recursively walked."""
        sub = make_module_named("myapp.submodule")
        mod = make_module_named("tests.example", sub=sub)
        result = detect_mocks_in_namespace(mod)
        # submodule is walked; no mocks, so result is empty
        assert result == []

    def test_avoids_revisiting_already_seen_modules(self) -> None:
        """Same module referenced twice is only walked once."""
        sub = make_module_named("myapp.shared")
        mod = make_module_named("tests.example", a=sub, b=sub)
        # should not infinite-loop; just returns empty (no mocks)
        result = detect_mocks_in_namespace(mod)
        assert result == []

    def test_getattr_exception_is_handled_gracefully(self) -> None:
        """Attributes that raise on access are silently skipped."""

        class Troublemaker:
            @property
            def explode(self) -> None:
                raise RuntimeError("boom")

        mod = make_module_named("tests.example", trouble=Troublemaker())
        # Should not raise; just returns empty
        result = detect_mocks_in_namespace(mod)
        assert result == []

    def test_detects_mock_in_non_exempt_submodule(self) -> None:
        """Mock objects inside a non-exempt submodule are detected."""
        sub = make_module_named("myapp.helpers", fake=Mock())
        mod = make_module_named("tests.example", sub=sub)
        result = detect_mocks_in_namespace(mod)
        assert any("fake" in item for item in result)

    def test_exempt_module_root_name_is_skipped_entirely(self) -> None:
        """A module whose own name is exempt (e.g. 'pytest.x') is skipped
        entirely — triggers the early return at line 18-19."""
        mod = make_module_named("pytest.some_helper")
        result = detect_mocks_in_namespace(mod)
        assert result == []

    def test_getattr_exception_during_walk_is_handled(self) -> None:
        """When getattr raises inside walk(), the exception is caught and
        the iteration continues."""

        class RaisesOnAccess:
            """Descriptor that raises when accessed."""

            def __get__(self, obj, objtype=None):
                raise RuntimeError("boom")

        import types as _types

        class RaisingModule(_types.ModuleType):
            raiser = RaisesOnAccess()

        mod = RaisingModule("tests.example")
        # dir() on the module will include 'raiser'
        result = detect_mocks_in_namespace(mod)
        # Should not raise; just returns whatever it found
        assert isinstance(result, list)
