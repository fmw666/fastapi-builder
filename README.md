# 「 FastAPI Builder 」

<div align="right">
    <a href="https://fastapi.tiangolo.com/zh/"><b>fastapi 官方网站 ➡</b></a>
</div>

<br>

> 💡 **fastapi 项目构建器. 一款帮助你快速构建 fastapi 项目的工具.**

&emsp;&emsp;fastapi-builder 是一个基于 FastAPI 框架的快速 Web 应用程序开发的工具箱。它提供了一组现成的工具和组件，可以帮助你快速构建具有良好结构和可维护性的 FastAPI Web 应用程序。其目的是提供一个一站式的解决方案，以加速快速原型开发和生产部署。

+ ***[特性](#-特性)***

+ ***[TODO](#-todo)***

+ ***[快速开始](#-快速开始)***

+ ***[项目结构](#-项目结构)***

+ ***[特别感谢](#-特别感谢)***

+ ***[许可证](#-许可证)***

<div align="center">
    <img src="https://github.com/fmw666/my-image-file/blob/master/images/cute/small-cute-8.jpg" width=100>
</div>

<br>

## 💬 特性

+ 参考 Django 化项目基础命令.

+ 创建可自定义的 project 项目.

+ 创建可定制的 app 应用.

+ 为您生成完整的项目结构.

+ 对数据库操作进行封装，便于轻松管理.

+ 支持数据库包括 Mysql.

+ 可选的配置如： Dockerfile、pre-commit.

+ 对虚拟环境进行管理.

<br>

## 🎯 TODO

<div align="right"><i><b><a href="#no-reply">PS: 期待您对本项目做出贡献...</a></b></i></div>

+ [ ] 持续完善项目框架代码部分

+ [ ] 持续完善项目框架文档部分

+ [x] 优化 requirements.txt

+ [x] 提供英文版本

+ [ ] 提供项目数据库 PostgreSQL 选项

+ [x] 提供完整的 run 方法

+ [x] 内置 alembic 数据迁移等管理

+ [x] 提供对运行环境的检查

+ [x] 提供 fastapi venv 命令，创建/开启/关闭虚拟环境

+ [x] 针对 Linux 环境提供支持

+ [x] 针对 Mac 环境提供支持

+ [x] 生成 app 时，自动注入到 project 中（路由管理分配）

<br>

## 🚀 快速开始

<div align="right">
<i>=> 依赖：<b>Python 3.6+</b></i>
<br>
<i>=> 详细教程：<b><a href="docs/tutorial.md">tutorial</a></b></i>
</div>
<br>

安装 `fastapi-builder` 项目：

```sh
pip install fastapi-builder
```

查看项目版本：

```sh
fastapi --version
```

项目帮助：

```sh
fastapi --help
fastapi startproject --help
```

创建 `fastapi` 项目：

```sh
fastapi startproject [name]

# or 带有交互选择

fastapi startproject [name] --interactive
```

创建 `fastapi` 应用：

```sh
fastapi startapp [name]
```

运行 `fastapi` 项目：

```sh
fastapi run
```

通过访问 `http://127.0.0.1:8000/docs` 以确保 fastapi 服务正常运行.

<br>

## 📁 项目结构

```c
.
├── alembic/                      - 数据库迁移工具
├── api/                          - web 相关（路由、认证、请求、响应）.
│   ├── errors/                   - 定义错误处理方法.
│   │   ├── http_error.py         - http 错误处理方法
│   │   │── validation_error.py   - 验证错误处理方法
│   ├── routes/                   - web routes 路由.
│   │   ├── api.py                - 总路由接口
│   │   └── authentication.py     - 认证相关（登录、注册）路由
├── app_user/                     - user 应用.
│   ├── api.py                    - 提供 user 接口方法
│   ├── model.py                  - 提供 user 表模型
│   ├── schema.py                 - 提供 user 结构模型
├── core/                         - 项目核心配置, 如: 配置文件, 事件句柄, 日志.
│   ├── .env                      - 配置文件.
│   ├── config.py                 - 解析配置文件, 用于其他文件读取配置.
│   ├── events.py                 - 定义 fastapi 事件句柄.
│   ├── logger.py                 - 定义项目日志方法.
├── db/                           - 数据库相关.
│   ├── base.py                   - 导入所有应用 model.
│   └── database.py               - sqlalchemy 方法应用.
│   ├── errors.py                 - 数据库相关错误异常.
│   ├── events.py                 - 数据库相关事件句柄.
├── lib/                          - 自定义库
│   ├── jwt.py                    - 用户认证 jwt 方法.
│   ├── security.py               - 加密相关方法.
├── logs/                         - 日志文件目录.
├── middleware/                   - 项目中间件.
│   ├── logger.py                 - 请求日志处理.
├── models/                       - sqlalchemy 基础模型相关
│   ├── base.py                   - sqlalchemy declarative Base 表模型.
│   └── mixins.py                 - mixin 抽象模型定义.
├── schemas/                      - pydantic 结构模型相关.
│   ├── auth.py                   - 用户认证相关结构模型.
│   └── base.py                   - pydantic 结构模型基础类.
│   ├── jwt.py                    - jwt 相关结构模型.
├── utils/                        - 工具类.
│   ├── consts.py                 - 项目常量定义.
│   ├── dbmanager.py              - 数据库管理服务.
│   ├── docs.py                   - fastapi docs 文档自定义.
├── .pre-commit-config.yaml       - pre-commit 配置文件.
├── alembic.ini                   - alembic 数据库迁移工具配置文件.
├── docker-compose.yaml           - docker 配置.
├── Dockerfile                    - dockfile 文件.
├── .fastapi-builder.ini          - fastapi-builder 配置文件.
├── LICENSE                       - 许可证信息.
├── main.py                       - fastapi application 创建和配置.
├── pyproject.toml                - poetry 需求模块信息.
├── README.md                     - 项目说明文档.
├── requirements.txt              - pip 需求模块信息.
└── setup.cfg                     - pre-commit 配置文件.
```

<br>

## ⚡ 特别感谢

项目配置生成及 questionary 内容基于项目：<https://github.com/ycd/manage-fastapi>

fastapi 项目基础框架参考：<https://github.com/nsidnev/fastapi-realworld-example-app/>

<br>

## 🚩 许可证

项目根据麻省理工学院的许可条款授权.
