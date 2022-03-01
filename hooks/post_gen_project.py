"""Script that runs after the project generation phase."""
import subprocess
from pathlib import Path

PROJECT_DIRECTORY = Path.cwd()


if "{{cookiecutter.python_version}}" != "3.8":
    (PROJECT_DIRECTORY / "poetry.lock").unlink()

subprocess.call(["git", "init"])
subprocess.call(["poetry", "install"])
subprocess.call(["poetry", "run", "pre-commit", "install"])
subprocess.call(["git", "add", "*"])
subprocess.call(["poetry", "run", "pre-commit", "run", "--all-files"])
subprocess.call(["git", "add", "*"])
subprocess.call(["poetry", "run", "git", "commit", "-m", "Initial commit"])
subprocess.call(["poetry", "shell"])