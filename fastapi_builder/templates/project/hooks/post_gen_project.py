import os


# 删除指定文件或目录
def remove_paths(paths: list):
    base_dir = os.getcwd()

    for path in paths:
        path = os.path.join(base_dir, path)
        if path and os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.unlink(path)

# 删除多余的文件
def del_redundant_file():
    remove_paths(["__init__.py"])

# 打包工具选择
def set_packaging():
    packaging = "{{ cookiecutter.packaging }}"
    if packaging == "pip":
        remove_paths(["poetry.lock", "pyproject.toml"])
    elif packaging == "poetry":
        remove_paths(["requirements.txt"])

# pre_commit 选择
def set_pre_commit():
    pre_commit: bool = eval("{{ cookiecutter.pre_commit }}")
    if pre_commit is False:
        remove_paths([".pre-commit-config.yaml", "setup.cfg"])

# docker 选择
def set_docker():
    docker: bool = eval("{{ cookiecutter.docker }}")
    if docker is False:
        remove_paths(["Dockerfile", "docker-compose.yaml"])

# 许可证选择
def set_license():
    license_ = "{{ cookiecutter.license }}"
    if license_ == "None":
        remove_paths(["LICENSE"])

# README 选择
def set_readme():
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
