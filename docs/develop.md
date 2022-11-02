### 本地调试及测试

本地安装：

```sh
# OS-windows cmd
$ pip install virtualenv   # 您的 python 版本需要 ≥ 3.6
$ virtualenv venv          # 创建虚拟环境
$ .\venv\Scripts\activate  # 启动虚拟环境

(venv)$ python .\setup.py bdist_wheel  # 打包
(venv)$ pip install .\dist\fastapi_builder-x.x.x-py3-none-any.whl

# 注意，当该虚拟环境下已经存在 fastapi-builder 模块，需先卸载重新安装
```

本地测试：

```sh
$ python tests/test_startapp.py
$ python tests/test_startproject.py
$ python tests/test_all
```

### 命令详解

**startproject**

+ 创建项目、定义数据库名
+ 将配置项信息写入到 .fastapi-builder 文件中，方便后续读取

**startapp**

+ 创建 app

**venv**

+ create：创建虚拟环境

+ on：开启虚拟环境

+ off：关闭虚拟环境

**run**

+ 每次运行读取 .fastapi-builder 检查是否是第一次运行

+ 若第一次运行，会自动 运行 --config 进行配置

+ --check：检查 moudle、数据库

+ --config：配置
    + 0）读取 .fastapi-builder，获取虚拟环境、打包方式、数据库等信息
    + 1）检查是否在虚拟环境下，没有的话会检查是否存在虚拟环境，若不存在，询问用户是否创建
    + 2）进入虚拟环境
    + 3）安装 requirements.txt
    + 4）检查数据库连接，若失败，让用户填写数据库地址、用户名、端口。重复检查直到连接
    + 5）创建数据库并运行迁移文件，创建相应的表
