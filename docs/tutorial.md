
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


### 虚拟环境管理

> 注意，我们并不会为您提供包管理相关帮助，因为我们认为您可以使用 pip 或 poetry 去管理，并且我们认为在相关方面，这两个工具在它们能力范围内已经足够成熟

调用创建虚拟环境命令，我们将在当前路径下创建一个名为 `venv` 的虚拟环境

```sh
$ fastapi venv create
```

当然，您也可以自定义虚拟环境名称，只不过我们推荐这个名称为 `venv`

> 注意，请在命名时带上 env 名称，否则管理器将不会搜寻到该虚拟环境

```sh
$ fastapi venv create --name=my_env
```

```sh
$ fastapi venv on   # 开启虚拟环境
$ fastapi venv off  # 关闭虚拟环境
```

### 项目的运行

❗ 您必须在创建好的项目根目录下执行该命令

```sh
$ fastapi run
```

> 所有项目当创建后首次运行时，fastapi-builder 会自动配置环境

当然，项目的运行可能出现异常情况，您可以通过 `--check` 参数检查运行环境

```sh
$ fastapi run --check
```

我们也提供针对错误环境的修正，您只需要通过 `--config` 来进行环境配置

```sh
$ fastapi run --config
```

要查看帮助可以使用 `--help` 选项

```sh
$ fastapi run --help
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

### 数据迁移管理

fastapi-builder 内置 alembic 作为项目数据库迁移工具，我们提供了两条基础指令来帮助完成迁移文件的生成和执行：

生成迁移文件

```sh
$ fastapi db makemigrations
```

生成迁移文件时，往往用户要提供 message 信息（默认为 "create migration"）

```sh
$ fastapi db makemigrations -m="here is the message"
```

执行迁移文件

```sh
$ fastapi db migrate
```
