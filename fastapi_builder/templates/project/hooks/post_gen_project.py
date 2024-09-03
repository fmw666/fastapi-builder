import os
from typing import List


def remove_paths(paths: List[str]) -> None:
    """
    删除指定文件或目录

    Args:
        paths (List[str]): 文件或目录路径列表
    """
    base_dir = os.getcwd()

    for path in paths:
        path = os.path.join(base_dir, path)
        if path and os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.unlink(path)


def del_redundant_file() -> None:
    """删除多余的文件"""
    remove_paths(["__init__.py"])


def set_packaging() -> None:
    """打包工具的选择"""
    packaging = "{{ cookiecutter.packaging }}"
    if packaging == "pip":
        remove_paths(["poetry.lock", "pyproject.toml"])
    elif packaging == "poetry":
        remove_paths(["requirements.txt"])


def set_pre_commit():
    """pre commit 的选择"""
    pre_commit: bool = eval("{{ cookiecutter.pre_commit }}")
    if pre_commit is False:
        remove_paths([".pre-commit-config.yaml", "setup.cfg"])


def set_docker():
    """docker 的选择"""
    docker: bool = eval("{{ cookiecutter.docker }}")
    if docker is False:
        remove_paths(["Dockerfile", "docker-compose.yaml"])


def set_license():
    """许可证的选择"""
    license_ = "{{ cookiecutter.license }}"
    if license_ == "None":
        remove_paths(["LICENSE"])


def set_readme():
    """README 的选择"""
    language = "{{ cookiecutter.language }}"
    if language == "cn":
        remove_paths(["README_EN.md"])
    else:
        remove_paths(["README.md"])
        # 将 README_EN 重命名为 README
        os.rename("README_EN.md", "README.md")


def main():
    del_redundant_file()
    set_docker()
    set_license()
    set_pre_commit()
    set_packaging()
    set_readme()


if __name__ == "__main__":
    main()
