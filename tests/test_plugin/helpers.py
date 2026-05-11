PYPROJECT_TEMPLATE = """\
[tool.pytest_layer_decorators]
domain_modules = ["fake_app.domain.*"]
application_modules = ["fake_app.application.*"]
infrastructure_modules = ["fake_app.infrastructure.*"]
presentation_modules = ["fake_app.presentation.*"]
"""

DOMAIN_MODEL = "class DomainEntity:\n    pass\n"
APP_USECASE = "class CreateUserUseCase:\n    pass\n"
INFRA_DB = "class Database:\n    pass\n"
PRES_API = "class ApiController:\n    pass\n"


def setup_fake_project(pytester) -> None:
    pytester.makepyprojecttoml(PYPROJECT_TEMPLATE)
    pytester.mkdir("fake_app")
    pytester.mkdir("fake_app/domain")
    pytester.mkdir("fake_app/application")
    pytester.mkdir("fake_app/infrastructure")
    pytester.mkdir("fake_app/presentation")
    pytester.makepyfile(**{
        "fake_app/__init__": "",
        "fake_app/domain/__init__": "",
        "fake_app/domain/models": DOMAIN_MODEL,
        "fake_app/application/__init__": "",
        "fake_app/application/usecases": APP_USECASE,
        "fake_app/infrastructure/__init__": "",
        "fake_app/infrastructure/db": INFRA_DB,
        "fake_app/presentation/__init__": "",
        "fake_app/presentation/api": PRES_API,
    })
