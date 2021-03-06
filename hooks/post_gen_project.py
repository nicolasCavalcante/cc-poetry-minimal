"""Script that runs after the project generation phase."""
import platform
import subprocess

if platform.system() == "Windows":
    env_str = subprocess.check_output(
        'py -{{cookiecutter.python_version}} -c "import sys;print(sys.executable)"',
        encoding="utf-8",
    ).strip()
else:
    env_str = "{{cookiecutter.python_version}}"

subprocess.call(["git", "init"])
subprocess.call(["poetry", "env", "use", env_str])
subprocess.call(["poetry", "install"])
subprocess.call(["poetry", "run", "pre-commit", "install"])
subprocess.call(["poetry", "run", "pre-commit", "install", "-t", "pre-push"])
subprocess.call(["git", "add", "*"])
subprocess.call(["poetry", "run", "pre-commit", "run", "--all-files"])
subprocess.call(["git", "add", "*"])
subprocess.call(["poetry", "run", "git", "commit", "-m", "Initial commit"])
subprocess.call(["poetry", "shell"])
