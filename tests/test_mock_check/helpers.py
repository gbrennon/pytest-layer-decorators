import types


def make_module_named(name: str, **attrs: object) -> types.ModuleType:
    mod = types.ModuleType(name)
    mod.__dict__.update(attrs)
    return mod
