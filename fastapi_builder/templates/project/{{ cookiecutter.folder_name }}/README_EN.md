# 「 {{ cookiecutter.name }} 」

<div align="right">
    <a href="https://github.com/fmw666/fastapi-builder/"><b>fastapi-builder official website ➡</b></a>
</div>

<br>

> 💡 **帮助您快速构建 fastapi 项目.**

+ ***[快速启用](#-快速启用)***

+ ***[项目结构](#-项目结构)***

+ ***[功能示例](#-功能示例)***

<div align="center">
    <img src="https://github.com/fmw666/my-image-file/blob/master/images/cute/small-cute-8.jpg" width=100>
</div>

<br>

## 🚀 快速启用

<http://127.0.0.1:8000/docs>：访问 swagger-ui 文档

**使用 fastapi-builder 工具**

我们更推荐您安装并使用 fastapi-builder 工具

如果您需要快速启动项目，使用 `fastapi run`

如果您需要检查项目配置，使用 `fastapi run --check`

如果您需要快速配置项目，使用 `fastapi run --config`

*当使用 fastapi-builder 工具后，您可以忽略下面操作。*

**1. 修改项目配置**

> 想要运行本项目，配置信息应该是您首先要关注的。

```js
project
├── core/
│   ├── .env     // 项目整体配置
├── alembic.ini  // 数据迁移配置
```

```s
# core/.env
DB_CONNECTION=mysql+pymysql://username:password@127.0.0.1:3306/dbname
SECRET_KEY=OauIrgmfnwCdxMBWpzPF7vfNzga1JVoiJi0hqz3fzkY


# alembic.ini
...
# 第 53 行，值同 .env 文件中 DB_CONNECTION
sqlalchemy.url = mysql+pymysql://root:admin@localhost/dbname
```
    
*（当您开始尝试阅读 [server/core/config.py](#no-reply) 文件后，您可以开始编写更多相关配置）*

**2. 启用数据库**

最后，您需要在环境中正确启动 mysql 服务，创建一个数据库，并执行迁移文件完成数据库中表的建立.<br>
幸运的是，这一点我们已经尽可能地为您考虑。您只需要正确启动 mysql 服务，并在 [app/utils/](#no-reply) 中执行：

```sh
project\utils> python dbmanager.py
```

**3. 运行项目**

```sh
project> python main.py
```

<br>

## 📌 项目结构

```js
project
├── alembic/                      - 数据库迁移工具
│   ├── versions/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
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
{% if cookiecutter.pre_commit == "True" -%}
├── .pre-commit-config.yaml       - pre-commit 配置文件.
{%- endif %}
├── alembic.ini                   - alembic 数据库迁移工具配置文件.
{% if cookiecutter.docker == "True" -%}
├── docker-compose.yaml           - docker 配置.
├── Dockerfile                    - dockfile 文件.
{%- endif -%}
{% if cookiecutter.license -%}
├── LICENSE                       - 许可证信息.
{%- endif %}
├── main.py                       - fastapi application 创建和配置.
{% if cookiecutter.packaging == "poetry" -%}
├── pyproject.toml                - poetry 需求模块信息.
{%- endif %}
├── README.md                     - 项目说明文档.
{% if cookiecutter.packaging == "pip" -%}
├── requirements.txt              - pip 需求模块信息.
{%- endif %}
{%- if cookiecutter.pre_commit == "True" -%}
├── setup.cfg                     - pre-commit 配置文件.
{%- endif %}
```

<br>

## 💬 功能示例

Swagger docs

<br>

## License

This project is licensed under the terms of the {{ cookiecutter.license }} license.
