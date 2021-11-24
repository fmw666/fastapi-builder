# fastapi-project-basis

> 帮助您快速构建 fastapi 项目.

## 🚀 快速启用

### 1、启用虚拟环境

项目中使用虚拟环境是必要的，我们也强烈建议您通过虚拟环境来开发您的项目

```sh
# cmd
server> pip install virtualenv   # 您的 python 版本需要 ≥ 3.7
server> virtualenv venv          # 创建虚拟环境
server> .\venv\Scripts\activate  # 启动虚拟环境

(venv) ...\server> pip install -r requirements.txt  # 安装必要模块
```

### 2、修改项目配置

想要运行本项目，配置信息应该是您首先要关注的：

在 server/core/ 中创建 .env 文件来编写项目的配置信息

```js
server
├── core/
│   ├── .env  # 这是您需要创建的文件
```

> 注意，文件包含后缀，完整命名即为 .env

正确创建完文件后，我们需要您写入至少如下内容（它们是以键值对形式存在，并且都为字符串类型，不需要引号）：

```s
DB_CONNECTION=mysql+pymysql://username:password@127.0.0.1:3306/dbname
SECRET_KEY=OauIrgmfnwCdxMBWpzPF7vfNzga1JVoiJi0hqz3fzkY
```

很显然，第一行为数据库连接信息，请正确输入您 mysql 服务用户名、密码、主机地址、端口号、数据库名等内容
第二行为密钥，您应该通过正确的方式为自己产品生成一串密钥，并填入其中

*（当您开始尝试阅读 server/core/config.py 文件后，您可以开始编写更多相关配置）*

+ config.py 文件已经基本满足项目所需的所有配置信息，但是对于迁移工具 alembic 我们还需要单独为其写入配置
    
    打开 server/alembic.ini 文件，在第 53 行 sqlalchemy.url 写入第一点中 DB_CONNECTION 后面内容即可。

### 3、启用数据库

最后，您需要在环境中正确启动 mysql 服务，创建一个数据库，并执行迁移文件

幸运的是，这一点我们已经尽可能地为您考虑。您只需要正确启动 mysql 服务，并在 server/scripts/ 中执行：

```sh
server\scripts> python mysqlservice.py
```

<br>

+ 请仔细阅读并执行完上面内容后，执行如下命令：

    ```sh
    server> python main.py
    ```

<br>

## 📌 项目结构

```js
server
├── api/              - web related stuff.
│   ├── errors/       - definition of error handlers.
│   └── routes/       - web routes.
├── core/             - application configuration, startup events, logging.
├── db/               - db related stuff.
│   ├── migrations/   - manually written alembic migrations.
│   └── repositories/ - all crud stuff.
├── lib/              - db related stuff.
├── models/           - pydantic models for this application.
│   ├── domain/       - main models that are used almost everywhere.
│   └── schemas/      - schemas for using in web routes.
├── utils/            - strings that are used in web responses.
├── ├── consts.py     - logic that is not just crud related.
└── main.py           - FastAPI application creation and configuration.
```