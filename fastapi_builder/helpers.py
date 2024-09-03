import re
from typing import TypeVar

import questionary

EnumType = TypeVar("EnumType")


def camel_to_snake(text: str) -> str:
    """驼峰命名转蛇形命名"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def snake_to_camel(text: str) -> str:
    """蛇形命名转驼峰命名"""
    return text.split("_")[0] + "".join(x.title() for x in text.split("_")[1:])


def camel_to_pascal(text: str) -> str:
    """驼峰命名转帕斯卡命名"""
    return text[0].upper() + text[1:]


def question(choices: EnumType) -> questionary.Question:
    prompt = camel_to_snake(choices.__name__).replace("_", " ")
    return questionary.select(
        f"Select the {prompt}: ", choices=[c.value for c in choices]
    )


def binary_question(option: str) -> questionary.Question:
    return questionary.confirm(f"Do you want {option}?", default=False)


def text_question(default: str) -> questionary.Question:
    return questionary.text(
        "The name of the database you want to create? ", default=default
    )
