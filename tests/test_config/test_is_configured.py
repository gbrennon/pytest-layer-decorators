from pytest_layer_decorators._config import is_configured


class TestIsConfigured:
    def test_empty_dict_is_not_configured(self) -> None:
        assert is_configured({}) is False

    def test_empty_lists_are_not_configured(self) -> None:
        assert is_configured({"domain": [], "application": []}) is False

    def test_non_empty_patterns_is_configured(self) -> None:
        assert is_configured({"domain": ["myapp.domain*"]}) is True
