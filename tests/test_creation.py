"""Test the creation of the project."""
import shutil
import stat
from pathlib import Path

import pytest
from cookiecutter import main

FOLDERS = [
    Path(".brainstorm"),
    Path(".git"),
    Path(".vscode"),
    Path("project_name"),
    Path("tests"),
]
FILES = [
    ".brainstorm/.gitignore",
    ".vscode/launch.json",
    ".vscode/settings.json",
    ".flake8",
    ".gitignore",
    ".pre-commit-config.yaml",
    "poetry.lock",
    "README.md",
    "poe_scripts.py",
    "pyproject.toml",
]

CC_ROOT = Path(__file__).parents[1].resolve()


def on_rm_error(func, path: str, exc_info):
    # from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows # noqa: E501
    path: Path = Path(path)
    path.chmod(stat.S_IWRITE)
    path.unlink()


@pytest.fixture(scope="function", name="project_dir")
def default_baked_project(tmp_path: Path):
    """Fixture for creation and teardown of the project."""
    out_dir = tmp_path / "project"
    out_dir.mkdir()

    main.cookiecutter(
        CC_ROOT.as_posix(),
        no_input=True,
        output_dir=out_dir,
    )

    # default project name is project_name
    yield out_dir / "project_name"

    # cleanup after
    shutil.rmtree(out_dir, onerror=on_rm_error)


def test_files(project_dir: Path):
    """Are the files there?"""
    for file_path in FILES:
        final_path = project_dir / file_path
        final_short = final_path.relative_to(final_path.parents[2])
        assert final_path.is_file(), f"{final_short} is missing"
        assert no_curlies(final_path), f"{final_short} has curly braces"


def test_folders(project_dir: Path):
    """Are the folders there?"""
    for folder in FOLDERS:
        final_path = project_dir / folder
        final_short = final_path.relative_to(final_path.parents[2])
        assert final_path.is_dir(), f"{final_short} is missing"
        assert no_curlies(final_path), f"{final_short} has curly braces"


def no_curlies(filepath: Path):
    """Utility to make sure no curly braces appear in a file.
    That is, was jinja able to render everthing?"""
    template_strings = ["{{", "}}", "{%", "%}"]

    if any([s in filepath.name for s in template_strings]):
        return False

    if filepath.is_file():
        template_strings_in_file = [s in filepath.read_text() for s in template_strings]
        return not any(template_strings_in_file)

    return True
