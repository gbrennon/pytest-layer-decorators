from types import ModuleType
from unittest.mock import NonCallableMock

from pytest_layer_decorators._exempt import is_module_exempt

_MOCK_PREFIXES = ("unittest.mock", "mock", "pytest_mock")


def detect_mocks_in_namespace(test_module: ModuleType) -> list[str]:
    found: list[str] = []
    visited: set[int] = set()

    def walk(mod: ModuleType) -> None:
        if id(mod) in visited:
            return
        visited.add(id(mod))
        mod_name = getattr(mod, "__name__", "")
        if is_module_exempt(mod_name):
            return
        for attr_name in dir(mod):
            try:
                obj = getattr(mod, attr_name)
            except Exception:
                continue
            if isinstance(obj, ModuleType):
                obj_name = getattr(obj, "__name__", "")
                if _belongs_to_mock_library(obj_name):
                    found.append(obj_name)
                if not is_module_exempt(obj_name):
                    walk(obj)
                continue
            if isinstance(obj, NonCallableMock):
                found.append(f"mock object '{attr_name}'")
                continue
            origin = getattr(obj, "__module__", None)
            if isinstance(origin, str) and _belongs_to_mock_library(origin):
                found.append(f"mock import '{attr_name}' (from {origin})")

    walk(test_module)
    return found


def _belongs_to_mock_library(module_name: str) -> bool:
    for prefix in _MOCK_PREFIXES:
        if module_name == prefix or module_name.startswith(prefix + "."):
            return True
    return False


def load_mock_policy(pytest_config: object | None = None) -> dict[str, bool]:
    from pytest_layer_decorators._config import _DEFAULT_LAYER_NAMES, _load_raw_pyproject_config

    policy: dict[str, bool] = {
        "domain": True,
        "application": True,
        "infrastructure": True,
        "presentation": True,
    }

    if pytest_config is not None and hasattr(pytest_config, "getini"):
        for layer in policy:
            val = _ini_bool(pytest_config, f"layer_{layer}_allow_mocks")  # type: ignore[arg-type]
            if val is not None:
                policy[layer] = val
        return policy

    pyproject = _load_raw_pyproject_config()
    if pyproject:
        allow_mocks = pyproject.get("allow_mocks")
        if isinstance(allow_mocks, dict):
            for layer in _DEFAULT_LAYER_NAMES:
                if layer in allow_mocks and isinstance(allow_mocks[layer], bool):
                    policy[layer] = allow_mocks[layer]

    return policy


def _ini_bool(config: object, key: str) -> bool | None:
    try:
        value = config.getini(key)  # type: ignore[attr-defined]
    except Exception:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes")
    if isinstance(value, list) and value:
        return str(value[0]).lower() in ("true", "1", "yes")
    return None
