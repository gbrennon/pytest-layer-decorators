import tomllib
from collections.abc import MutableMapping
from pathlib import Path

_DEFAULT_LAYER_NAMES = ("domain", "application", "infrastructure", "presentation")

_ALLOWED_IMPORTS_BY_LAYER: dict[str, set[str]] = {
    "domain": set(),
    "application": {"domain"},
    "infrastructure": {"domain", "application"},
    "presentation": {"domain", "application"},
}


def load_config(pytest_config: object | None = None) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}

    if pytest_config is not None and hasattr(pytest_config, "getini"):
        for layer in _DEFAULT_LAYER_NAMES:
            patterns = _parse_ini_value(pytest_config, f"layer_{layer}_modules")  # type: ignore[arg-type]
            if patterns is not None:
                result[layer] = patterns

    if not result:
        pyproject = _load_from_pyproject()
        if pyproject:
            for layer in _DEFAULT_LAYER_NAMES:
                patterns = _extract_patterns(pyproject.get(f"{layer}_modules"))
                if patterns:
                    result[layer] = patterns

    return result


def _load_from_pyproject() -> dict[str, list[str]] | None:
    candidate = Path.cwd()
    for _ in range(20):
        pyproject = candidate / "pyproject.toml"
        if pyproject.is_file():
            raw = pyproject.read_bytes()
            data = tomllib.loads(raw.decode("utf-8"))
            tool = data.get("tool", {})
            cfg = tool.get("pytest_layer_decorators", {})
            if isinstance(cfg, dict):
                return {k: v for k, v in cfg.items() if isinstance(v, list)}
            break
        if candidate.parent == candidate:
            break
        candidate = candidate.parent
    return None


def _extract_patterns(value: object) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        return value  # type: ignore[return-value]
    if isinstance(value, str):
        return [value]
    return None


def _parse_ini_value(
    config: MutableMapping[str, str | list[str]], key: str,
) -> list[str] | None:
    value = config.getini(key)  # type: ignore[attr-defined]
    if not value:
        return None
    if isinstance(value, list):
        if all(isinstance(x, str) for x in value):
            return value  # type: ignore[return-value]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return None


def get_allowed_layers(layer: str) -> set[str]:
    return _ALLOWED_IMPORTS_BY_LAYER.get(layer, set())


def get_layer_names() -> tuple[str, ...]:
    return _DEFAULT_LAYER_NAMES


def is_configured(config: dict[str, list[str]]) -> bool:
    return any(v for v in config.values())


def _load_raw_pyproject_config() -> dict[str, object] | None:
    candidate = Path.cwd()
    for _ in range(20):
        pyproject = candidate / "pyproject.toml"
        if pyproject.is_file():
            raw = pyproject.read_bytes()
            data = tomllib.loads(raw.decode("utf-8"))
            tool = data.get("tool", {})
            cfg = tool.get("pytest_layer_decorators", {})
            if isinstance(cfg, dict):
                return cfg
            return None
        if candidate.parent == candidate:
            break
        candidate = candidate.parent
    return None
