import sys

from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item

_ENFORCED_LAYER_NAMES = ("domain", "application", "infrastructure", "presentation")


def pytest_addoption(parser: Parser) -> None:
    parser.getgroup("pytest_layer_decorators", "Layer separation enforcement")
    for layer_name in _ENFORCED_LAYER_NAMES:
        parser.addini(
            f"layer_{layer_name}_modules",
            f"Glob-style module patterns for the {layer_name} layer",
            type="linelist",
            default=[],
        )
        parser.addini(
            f"layer_{layer_name}_allow_mocks",
            f"Whether mocks are allowed in @{layer_name} tests (default: true)",
            type="bool",
            default=True,
        )


def pytest_configure(config: Config) -> None:
    for layer_name in _ENFORCED_LAYER_NAMES:
        config.addinivalue_line(
            "markers",
            f"{layer_name}: mark test as belonging to the {layer_name} layer",
        )


def pytest_report_header(config: Config) -> str | None:
    from pytest_layer_decorators._config import is_configured, load_config
    cfg = load_config(config)
    if is_configured(cfg):
        return f"pytest-layer-decorators: enforcing layers: {', '.join(sorted(cfg))}"
    return "pytest-layer-decorators: no layer patterns configured — enforcement disabled"


def resolve_test_module_from_item(item: Item) -> object | None:
    node: object = item
    for _ in range(20):
        parent: object = getattr(node, "parent", None)
        if parent is None:
            nodeid: str = getattr(item, "nodeid", "")
            parts = nodeid.split("::", 1)
            if parts:
                mod_path = parts[0].replace("/", ".").removesuffix(".py")
                return sys.modules.get(mod_path)
            return None
        obj = getattr(parent, "obj", None)
        if isinstance(obj, type(sys)) and hasattr(obj, "__name__"):
            return obj
        node = parent
    return None


def pytest_runtest_setup(item: Item) -> None:
    import pytest
    from pytest_layer_decorators._config import is_configured, load_config
    from pytest_layer_decorators._mock_check import detect_mocks_in_namespace, load_mock_policy
    from pytest_layer_decorators._rules import check_layer_rules

    cfg = load_config(item.config)
    if not is_configured(cfg):
        return

    item_layer_names = set(_ENFORCED_LAYER_NAMES) & {m.name for m in item.iter_markers()}
    if not item_layer_names:
        return

    test_module = resolve_test_module_from_item(item)
    if test_module is None or not isinstance(test_module, type(sys)):
        return

    mock_policy = load_mock_policy(item.config)
    nodeid = getattr(item, "nodeid", str(item))

    for layer in item_layer_names:
        violations = check_layer_rules(test_module, layer, cfg)  # type: ignore[arg-type]
        if violations:
            pytest.fail(
                format_violation_message(nodeid, layer, violations),
                pytrace=False,
            )

        if not mock_policy.get(layer, True):
            mock_evidence = detect_mocks_in_namespace(test_module)  # type: ignore[arg-type]
            if mock_evidence:
                pytest.fail(
                    format_mock_violation_message(nodeid, layer, mock_evidence),
                    pytrace=False,
                )


def format_violation_message(nodeid: str, layer: str, violations: list[str]) -> str:
    return "\n".join([
        f"Layer violation in {nodeid}:",
        f"  test is marked @{layer} but imports from a restricted layer:",
        *violations,
        f"  @{layer} may only import from: {summarize_allowed_layers(layer)}",
    ])


def format_mock_violation_message(nodeid: str, layer: str, evidence: list[str]) -> str:
    return "\n".join([
        f"Mock violation in {nodeid}:",
        f"  test is marked @{layer} but mocks are disallowed for this layer:",
        *[f"  - {item}" for item in evidence],
    ])


def summarize_allowed_layers(layer: str) -> str:
    from pytest_layer_decorators._config import get_allowed_layers
    allowed = get_allowed_layers(layer)
    if not allowed:
        return "nothing outside its own layer"
    return ", ".join(sorted(allowed))
