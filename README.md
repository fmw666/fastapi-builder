# 「 FastAPI Builder 」

<div align="right">
    <a href="https://fastapi.tiangolo.com/zh/"><b>fastapi 官方网站 ➡</b></a>
</div>

<br>

> 💡 **fastapi 项目构建器. 一款帮助你快速构建 fastapi 项目的工具.**

+ ***[特性](#-特性)***

+ ***[TODO](#-todo)***

+ ***[快速开始](#-快速开始)***

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

+ [ ] 提供英文版本

+ [ ] 提供项目数据库 PostgreSQL 选项

+ [x] 提供完整的 run 方法

+ [ ] 内置 alembic 数据迁移等管理

+ [x] 提供对运行环境的检查

+ [x] 提供 fastapi venv 命令，创建/开启/关闭虚拟环境

+ [ ] 针对 Linux 环境提供支持

+ [ ] 针对 Mac 环境提供支持

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

<br>

## ⚡ 特别感谢

项目配置生成及 questionary 内容基于项目：<https://github.com/ycd/manage-fastapi>

fastapi 项目基础框架参考：<https://github.com/nsidnev/fastapi-realworld-example-app/>

<br>

## 🚩 许可证

项目根据麻省理工学院的许可条款授权.
