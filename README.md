# 「 FastAPI Builder 」

<div align="right">
    <a href="https://fastapi.tiangolo.com/zh/">fastapi 官方网站 ➡</a>
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

+ 创建可自定义的 project 项目.

+ 创建可定制的 app 应用.

+ 为您生成完整的项目结构.

+ 可选的 Dockerfile.

+ 可选的 pre-commit.

<br>

## 🎯 TODO

+ [ ] 提供英文版本

+ [ ] 提供项目数据库 Postgres 选项

<br>

## 🚀 快速开始

> 依赖：Python 3.6+

安装 fastapi-builder 项目：

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

创建 fastapi 项目：

```sh
fastapi startproject [name]

# or 带有交互选择

fastapi startproject [name] --interactive
```

创建 fastapi 应用：

```sh
fastapi startapp [name]
```

运行 fastapi 项目：

```sh
fastapi run
```

<br>

## ⚡ 特别感谢

项目配置生成及 questionary 内容基于项目：<https://github.com/ycd/manage-fastapi>

fastapi 项目基础框架参考：<https://github.com/nsidnev/fastapi-realworld-example-app/>

<br>

## 🚩 许可证

项目根据麻省理工学院的许可条款授权
