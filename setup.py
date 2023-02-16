# MIT License

# Copyright (c) 2021 fmw666

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup, find_packages


# 解析 readme.md 文件
with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

# 解析 requirements.txt 文件
with open("requirements.txt", "r", encoding="utf-8") as fp:
    install_requires = fp.read().split("\n")


setup(
    name="fastapi-builder",
    version="1.3.0",
    author="fmw666",
    author_email="fmw19990718@qq.com",
    description="fastapi-builder Project generator and manager for FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["fastapi", "builder"],
    # 项目主页
    url="https://github.com/fmw666/fastapi-builder",
    # 需要被打包的内容
    packages=find_packages(where=".", exclude=(), include=("*",)),
    include_package_data=True,
    package_data={"": ["*.*"]},
    exclude_package_data={"": ["*.pyc"]},
    # 许可证
    license="https://mit-license.org/",
    # 项目依赖
    install_requires=install_requires,
    # 支持自动生成脚本
    entry_points={
        "console_scripts": [
            "fastapi=fastapi_builder.__main__:main"
        ]
    },
    classifiers=[
        # 3-Alpha  4-Beta  5-Production/Stable
        "Development Status :: 3 - Alpha",
        # 目标用户: 开发者
        "Intended Audience :: Developers",
        # 类型: 软件
        "Topic :: Software Development :: Build Tools",
        # 许可证信息
        "License :: OSI Approved :: MIT License",
        # 目标 Python 版本
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        # 操作系统
        "Operating System :: OS Independent"
    ]
)

# how to upload to pypi?
# pip install twine==3.8.0
# pip install wheel==0.38.4
# 1. python .\setup.py sdist bdist_wheel
# 2. twine upload dist/*
