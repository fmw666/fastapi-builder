
## 🚀 使用教程

<br>

### 安装模块

```sh
$ pip install fastapi-builder
```

### 查看版本

```sh
$ fastapi --version
```

### 查看帮助

```sh
$ fastapi --help
```

### 项目的创建

对于快速创建一个项目您可以使用如下命令（假设您的项目名称为 test）：

```sh
$ fastapi startproject test
```

默认生成的项目配置如下：

+ 数据库：MySQL
+ 数据库名称：*同创建的项目名*
+ docker：不带有
+ license：不带有
+ 打包方式：pip
+ pre-commit：不带有
+ Python 版本：3.8

当然，也许你需要一些可自主配置的操作：

```sh
$ fastapi startproject test --database=mysql   # 数据库选择 mysql
$ fastapi startproject test --dbname=db_test   # 数据库名称定义
$ fastapi startproject test --docker           # docker 选择带有
$ fastapi startproject test --no-docker        # docker 选择不带有
$ fastapi startproject test --license=mit      # 协议选择 MIT
$ fastapi startproject test --packaging=pip    # 打包方式选择 pip
$ fastapi startproject test --pre-commit       # pre-commit 选择带有
$ fastapi startproject test --python=3.6       # python 版本选择 3.6
```

配置项可以任意搭配：

```sh
$ fastapi startproject test --docker --license=mit
```

配置项可以重复，均以最后一个为准（如下面命令依然创建了 dockerfile 文件）

```sh
$ fastapi startproject test --no-docker --docker
```

要查看帮助可以使用 `--help` 选项

```sh
$ fastapi startproject --help
```

当然，如果您要改的配置项较多，想要更灵活的方式，我们推荐您使用交互式的创建：

```sh
$ fastapi startproject test --interactive
```

### 应用的创建

❗ 您必须在创建好的项目根目录下执行该命令

```sh
$ fastapi startapp blog
```

我们也为您准备了强制命令，以便您能在任何地方创建应用（当然，我们并不推荐您这样做）

```sh
$ fastapi startapp blog --force
```

要查看帮助可以使用 `--help` 选项

```sh
$ fastapi startapp --help
```

### 数据库操作??

### 项目的运行

❗ 您必须在创建好的项目根目录下执行该命令

```sh
$ fastapi run
```

<hr>

**1. 启用虚拟环境**

项目中使用虚拟环境是必要的，我们也强烈建议您通过虚拟环境来开发您的项目：

```sh
# OS-windows cmd
$ pip install virtualenv   # 您的 python 版本需要 ≥ 3.6
$ virtualenv venv          # 创建虚拟环境
$ .\venv\Scripts\activate  # 启动虚拟环境

(venv)$ pip install fastapi-builder  # 安装模块
```