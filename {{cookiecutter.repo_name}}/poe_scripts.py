"""Scripts used on poe the poet module."""
import functools
import inspect
import subprocess
import webbrowser
from pathlib import Path

import fire
import typeguard

SELFPATH = Path(__file__).parent


def typechecked(func):
    __annotations__ = getattr(func, "__annotations__", None)
    if __annotations__:
        __signature__ = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return typeguard.typechecked(func)(*args, **kwargs)
            except TypeError as exc:
                err = str(exc)
                found = False
                for param in __signature__.parameters.values():
                    if f'type of argument "{param.name}" ' not in err:
                        continue
                    found = True
                    if (
                        param.kind == param.POSITIONAL_ONLY
                        or param.default == param.empty
                    ):
                        err = err.replace(param.name, param.name.upper())
                    elif param.kind in {
                        param.POSITIONAL_OR_KEYWORD,
                        param.KEYWORD_ONLY,
                    }:
                        err = err.replace(
                            param.name, f"--{param.name.replace('_', '-')}"
                        )
                if found:
                    raise fire.core.FireError(err)
                raise exc

        return wrapper
    return func


@typechecked
def coverage(skip_test: bool = False, in_browser: bool = False):
    """Runs test coverage and shows results"""
    if (not skip_test) or (not (SELFPATH / ".coverage").exists()):
        subprocess.run(["coverage", "run", "-m", "pytest"])
    if in_browser:
        if (not skip_test) or (not (SELFPATH / "htmlcov").exists()):
            subprocess.run(["coverage", "html"])
        webbrowser.open(SELFPATH.absolute() / "htmlcov/index.html")
    else:
        subprocess.run(["coverage", "report", "-m"])
