本地测试方法的方法

```sh
$ python tests/test_startapp.py
$ python tests/test_startproject.py
```

当作本地包测试方法

```sh
# OS-windows cmd
$ pip install virtualenv   # 您的 python 版本需要 ≥ 3.6
$ virtualenv venv          # 创建虚拟环境
$ .\venv\Scripts\activate  # 启动虚拟环境

(venv)$ python .\setup.py bdist_wheel  # 打包
(venv)$ pip install .\dist\fastapi_builder-x.x.x-py3-none-any.whl
```

在全局环境下可以进行测试
