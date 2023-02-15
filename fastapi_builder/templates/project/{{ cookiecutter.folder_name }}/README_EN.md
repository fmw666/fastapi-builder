# 「 {{ cookiecutter.name }} 」

<div align="right">
    <a href="https://github.com/fmw666/fastapi-builder/"><b>fastapi-builder Project URL ➡</b></a>
</div>

<br>

> 💡 Help you quickly build fastapi projects.

+ ***[Quick Start](#-Quick-Start)***

+ ***[Project Structure](#-Project-Structure)***

+ ***[Functional Examples](#-Functional-Examples)***

<div align="center">
    <img src="https://github.com/fmw666/my-image-file/blob/master/images/cute/small-cute-8.jpg" width=100>
</div>

<br>

## 🚀 Quick Start

> *We highly recommend you to install and use fastapi-builder tool.*<br>
> After the project is started, enter the address http://127.0.0.1:8000/docs in the browser to access the swagger-ui document.

### ⭐ Method 1: Use fastapi-builder tool

+ Quick start the project: `fastapi run`
+ Check project configuration: `fastapi run --check`
+ Quickly configure the project: `fastapi run --config`

*If you have not used fastapi-builder, try to manually complete the steps in method 2.*

### Method 2: Configure and Start the Project Manually

**1. Modify project configuration**

> To run this project, configuration information should be your first concern.

```js
project
├── core/
│   ├── .env     // Overall project configuration
├── alembic.ini  // Database migration configuration

```s
# core/.env
DB_CONNECTION=mysql+pymysql://username:password@127.0.0.1:3306/dbname
SECRET_KEY=OauIrgmfnwCdxMBWpzPF7vfNzga1JVoiJi0hqz3fzkY


# alembic.ini
...
# line 53, the same value as DB_CONNECTION in .env file
sqlalchemy.url = mysql+pymysql://root:admin@localhost/dbname
```

* (When you start reading the [server/core/config.py](#no-reply) file, you can start writing more related configurations)*

**2. Activate the Database**

Finally, you need to start the mysql service correctly in the environment, create a database, and execute the migration file to complete the creation of tables in the database. <br>
Fortunately, we have considered this as much as possible for you. You only need to correctly start the mysql service and execute it in [app/utils/](#no-reply):

```sh
project\utils> python dbmanager.py
```

**3. Run the project**

```sh
project> python main.py
```

<br>

## 📌 Project Structure

```js
project
├── alembic/                      - Database migration tool
│   ├── versions/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
├── api/                          - Web-related (routes, authentication, requests, responses).
│   ├── errors/                   - Defines error handling methods.
│   │   ├── http_error.py         - HTTP error handling method.
│   │   ├── validation_error.py   - Validation error handling method.
│   ├── routes/                   - Web routes.
│   │   ├── api.py                - Main route interface.
│   │   └── authentication.py     - Authentication-related (login, registration) routes.
├── app_user/                     - User application.
│   ├── api.py                    - Provides user interface methods.
│   ├── model.py                  - Provides user table model.
│   ├── schema.py                 - Provides user structure model.
├── core/                         - Project core configuration, such as: configuration files, event handlers, logging.
│   ├── .env                      - Configuration file.
│   ├── config.py                 - Parses the configuration file for other files to read the configuration.
│   ├── events.py                 - Defines fastapi event handlers.
│   ├── logger.py                 - Defines project logging methods.
├── db/                           - Database related.
│   ├── base.py                   - Imports all application models.
│   ├── database.py               - sqlalchemy method application.
│   ├── errors.py                 - Database-related error exceptions.
│   ├── events.py                 - Database-related event handlers.
├── lib/                          - Custom library.
│   ├── jwt.py                    - User authentication jwt method.
│   ├── security.py               - Encryption-related methods.
├── logs/                         - Directory for log files.
├── middleware/                   - Project middleware.
│   ├── logger.py                 - Request log processing.
├── models/                       - sqlalchemy basic model related.
│   ├── base.py                   - sqlalchemy declarative Base table model.
│   └── mixins.py                 - mixin abstract model definition.
├── schemas/                      - pydantic structure model related.
│   ├── auth.py                   - User authentication-related structure model.
│   └── base.py                   - pydantic structure model base class.
│   ├── jwt.py                    - jwt related structure model.
├── utils/                        - Utility classes.
│   ├── consts.py                 - Project constant definition.
│   ├── dbmanager.py              - Database management service.
│   ├── docs.py                   - Custom fastapi docs documentation.
{% if cookiecutter.pre_commit == "True" -%}
├── .pre-commit-config.yaml       - Pre-commit configuration file.
{%- endif %}
├── alembic.ini                   - alembic database migration tool configuration file.
{% if cookiecutter.docker == "True" -%}
├── docker-compose.yaml           - Docker configuration.
├── Dockerfile                    - Dockerfile.
{%- endif -%}
{% if cookiecutter.license -%}
├── LICENSE                       - License information.
{%- endif %}
├── main.py                       - fastapi application creation and configuration.
{% if cookiecutter.packaging == "poetry" -%}
├── pyproject.toml                - Poetry requirement module information.
{%- endif %}
├── README.md                     - Project description document.
{% if cookiecutter.packaging == "pip" -%}
├── requirements.txt              - Pip requirement module information.
{%- endif %}
{%- if cookiecutter.pre_commit == "True" -%}
├── setup.cfg                     - Pre-commit configuration file.
{%- endif %}
```

<br>

## 💬 Functional Examples

For details, see the Swagger docs after starting the project.

<br>

## License

This project is licensed under the terms of the {{ cookiecutter.license }} license.
