from pytest_layer_decorators._config import get_layer_names


class TestLayerNames:
    def test_returns_canonical_order(self) -> None:
        assert get_layer_names() == ("domain", "application", "infrastructure", "presentation")
