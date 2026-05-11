class TestNoConfigGracefulDegradation:
    def test_allows_any_import_when_no_config(self, pytester) -> None:
        pytester.mkdir("fake_app")
        pytester.mkdir("fake_app/infrastructure")
        pytester.makepyfile(**{
            "fake_app/__init__": "",
            "fake_app/infrastructure/__init__": "",
            "fake_app/infrastructure/db": "class Database:\n    pass\n",
        })
        pytester.makepyfile(test_any="""
            from pytest_layer_decorators import domain
            from fake_app.infrastructure.db import Database

            @domain
            def test_bad():
                assert Database() is not None
        """)
        result = pytester.runpytest("-v")
        result.assert_outcomes(passed=1)
