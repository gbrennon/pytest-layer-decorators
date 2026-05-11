# pytest-layer-decorators

Reusable [pytest](https://docs.pytest.org/) decorators that enforce **architectural layer separation** in test suites.

## Installation

```bash
pip install pytest-layer-decorators
```

## Quick Start

### 1. Configure your layer module patterns

In your `pyproject.toml`:

```toml
[tool.pytest_layer_decorators]
domain_modules        = ["myapp.domain.*"]
application_modules   = ["myapp.application.*"]
infrastructure_modules = ["myapp.infrastructure.*"]
presentation_modules  = ["myapp.presentation.*"]
```

Alternatively, in `pytest.ini`:

```ini
[pytest]
layer_domain_modules =
    myapp.domain.*
layer_application_modules =
    myapp.application.*
layer_infrastructure_modules =
    myapp.infrastructure.*
layer_presentation_modules =
    myapp.presentation.*
```

### 2. Decorate your tests

Apply the decorator directly to a test **function** or to a test **class** (the marker
propagates to every test method inside the class).

```python
from pytest_layer_decorators import domain, application, infrastructure, presentation

# ── style A: decorate individual test functions ──────────────────────

@domain
def test_entity_validation():
    from myapp.domain.models import Entity
    assert Entity("foo").name == "foo"

@application
def test_create_user_usecase():
    from myapp.domain.models import User
    from myapp.application.usecases import CreateUserUseCase
    ...

# ── style B: decorate a test class ───────────────────────────────────

@infrastructure
class TestDatabaseAdapter:
    def test_save(self):
        from myapp.infrastructure.db import Database
        ...

    def test_query(self):
        from myapp.infrastructure.db import Database
        ...

@presentation
class TestAPIController:
    def test_index_route(self):
        from myapp.presentation.api import UserController
        ...
```

### 3. Run pytest

Violations are reported at test setup time with clear messages:

```
ERROR test_domain.py::test_bad - Failed: Layer violation in test_domain.py::test_bad:
  test is marked @domain but imports from a restricted layer:
  - 'myapp.infrastructure.db' (belongs to 'infrastructure' layer, not allowed from 'domain' layer)
  @domain may only import from: nothing outside its own layer
```

## Layer Dependency Rules

| Layer | May import from |
|---|---|
| `@domain` | Nothing outside its own layer |
| `@application` | `domain` |
| `@infrastructure` | `domain`, `application` |
| `@presentation` | `domain`, `application` |

These rules mirror Clean Architecture / Hexagonal Architecture dependency flow:
dependencies point inward, from outer layers (presentation, infrastructure)
toward inner layers (application, domain).

## Graceful Degradation

If no layer patterns are configured, the decorators still apply pytest markers
but enforcement is **disabled** — no tests will be blocked. This allows
incremental adoption.

## License

MIT
