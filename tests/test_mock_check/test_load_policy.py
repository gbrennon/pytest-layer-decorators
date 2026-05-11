from pytest_layer_decorators._mock_check import load_mock_policy


class TestLoadMockPolicy:
    def test_defaults_all_true_when_no_config(self) -> None:
        policy = load_mock_policy(None)
        assert policy == {
            "domain": True,
            "application": True,
            "infrastructure": True,
            "presentation": True,
        }
