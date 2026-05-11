"""Decorator factories for layer enforcement.

Each decorator marks a test function with the corresponding pytest marker.
Full import validation happens later inside the pytest plugin hook
during collection (see _plugin.py).
"""

import functools
from collections.abc import Callable
from typing import Any, TypeVar

import pytest

F = TypeVar("F", bound=Callable[..., Any])


def _layer_decorator(layer_name: str) -> Callable[[F], F]:
    """Create a decorator that applies the *layer_name* marker.

    The marker is evaluated eagerly at decoration time.  Full import
    validation happens later inside the pytest plugin hook during
    collection (see _plugin.py).
    """

    marker = getattr(pytest.mark, layer_name)

    @functools.wraps(marker)  # type: ignore[arg-type]
    def decorator(func: F) -> F:
        return marker(func)  # type: ignore[return-value]

    # Attach metadata for introspection.
    decorator.__layer_name__ = layer_name  # type: ignore[attr-defined]
    return decorator


domain = _layer_decorator("domain")
application = _layer_decorator("application")
infrastructure = _layer_decorator("infrastructure")
presentation = _layer_decorator("presentation")
