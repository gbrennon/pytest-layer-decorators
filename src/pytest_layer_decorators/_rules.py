import fnmatch
from collections.abc import Iterable
from types import ModuleType

from pytest_layer_decorators._config import get_allowed_layers
from pytest_layer_decorators._exempt import is_module_exempt


def collect_imported_module_names(test_module: ModuleType) -> set[str]:
    module_names: set[str] = set()
    visited_module_ids: set[int] = set()

    def walk_namespace(mod: ModuleType) -> None:
        if id(mod) in visited_module_ids:
            return
        visited_module_ids.add(id(mod))
        for attr_name in dir(mod):
            try:
                obj = getattr(mod, attr_name)
            except Exception:
                continue
            if isinstance(obj, ModuleType):
                obj_name = getattr(obj, "__name__", "")
                if obj_name:
                    module_names.add(obj_name)
                    walk_namespace(obj)
                continue
            origin_module = getattr(obj, "__module__", None)
            if isinstance(origin_module, str) and origin_module:
                module_names.add(origin_module)
                module_names.add(origin_module.partition(".")[0])

    walk_namespace(test_module)
    return module_names


def module_name_matches_any_pattern(module_name: str, patterns: Iterable[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(module_name, pattern):
            return True
    return False


def check_layer_rules(
    test_module: ModuleType,
    layer: str,
    layer_patterns: dict[str, list[str]],
) -> list[str]:
    if not layer_patterns:
        return []

    allowed_layer_names = get_allowed_layers(layer)

    permitted_patterns: list[str] = []
    for allowed_layer in allowed_layer_names:
        permitted_patterns.extend(layer_patterns.get(allowed_layer, []))
    permitted_patterns.extend(layer_patterns.get(layer, []))

    restricted_patterns: list[tuple[str, str]] = []
    for other_layer, patterns in layer_patterns.items():
        if other_layer == layer or other_layer in allowed_layer_names:
            continue
        for pattern in patterns:
            restricted_patterns.append((other_layer, pattern))

    violations: list[str] = []
    imported_names = collect_imported_module_names(test_module)
    for module_name in sorted(imported_names):
        if is_module_exempt(module_name):
            continue
        if module_name_matches_any_pattern(module_name, permitted_patterns):
            continue
        for restricted_layer, restricted_pattern in restricted_patterns:
            if fnmatch.fnmatch(module_name, restricted_pattern):
                violations.append(
                    f"  - {module_name!r} (belongs to '{restricted_layer}' layer, "
                    f"not allowed from '{layer}' layer)"
                )
                break
    return violations
