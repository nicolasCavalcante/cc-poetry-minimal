"""Scripts used on poe the poet module."""
import shutil
import stat
from pathlib import Path

from cookiecutter import main

CC_ROOT = Path(__file__).parent.resolve()
BAKED = CC_ROOT / "baked"


def on_rm_error(func, path: str, exc_info):
    # from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows # noqa: E501
    path: Path = Path(path)
    path.chmod(stat.S_IWRITE)
    path.unlink()


def bake_project(input_dir: Path = CC_ROOT, output_dir: Path = BAKED):
    """Creates temporary project."""
    clean_project(output_dir)
    output_dir.mkdir()
    main.cookiecutter(
        input_dir.as_posix(),
        no_input=True,
        output_dir=output_dir,
    )


def clean_project(output_dir: Path = BAKED):
    """Cleans up temporary project."""
    if output_dir.exists():
        shutil.rmtree(output_dir / "", onerror=on_rm_error)
