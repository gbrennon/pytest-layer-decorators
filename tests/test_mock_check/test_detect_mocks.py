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
