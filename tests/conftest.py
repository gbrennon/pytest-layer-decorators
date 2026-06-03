pytest_plugins = ["pytester"]


def pytest_configure(config):
    config.addinivalue_line("markers", "test_layer: marker used in unit tests")
