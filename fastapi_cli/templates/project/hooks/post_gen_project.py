import os


def remove_paths(paths: list):
    base_dir = os.getcwd()

    for path in paths:
        path = os.path.join(base_dir, path)
        if path and os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.unlink(path)


def set_packaging():
    packaging = "{{ cookiecutter.packaging }}"
    if packaging == "pip":
        remove_paths(["poetry.lock", "pyproject.toml"])
    elif packaging == "poetry":
        remove_paths(["requirements.txt"])


def set_pre_commit():
    pre_commit: bool = eval("{{ cookiecutter.pre_commit }}")
    if pre_commit is False:
        remove_paths([".pre-commit-config.yaml", "setup.cfg"])


def set_docker():
    docker: bool = eval("{{ cookiecutter.docker }}")
    if docker is False:
        remove_paths(["Dockerfile", "docker-compose.yaml"])


def set_license():
    license_ = "{{ cookiecutter.license }}"
    if license_ == "None":
        remove_paths(["LICENSE"])


def main():
    set_docker()
    set_license()
    set_pre_commit()
    set_packaging()


if __name__ == "__main__":
    main()
