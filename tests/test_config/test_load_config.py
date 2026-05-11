import os
import textwrap

from pytest_layer_decorators._config import load_config


class TestLoadConfigWithoutPytest:
    def test_returns_empty_when_no_pyproject(self, tmp_path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            assert load_config(None) == {}
        finally:
            os.chdir(old_cwd)

    def test_loads_from_pyproject_toml(self, tmp_path) -> None:
        tmp_path.joinpath("pyproject.toml").write_text(textwrap.dedent("""\
            [tool.pytest_layer_decorators]
            domain_modules = ["myapp.domain.*"]
            application_modules = ["myapp.application.*"]
        """))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            assert load_config(None) == {
                "domain": ["myapp.domain.*"],
                "application": ["myapp.application.*"],
            }
        finally:
            os.chdir(old_cwd)
