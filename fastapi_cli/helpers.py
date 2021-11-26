import re
from typing import TypeVar

import questionary

EnumType = TypeVar("EnumType")


def camel_to_snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def snake_to_camel(text: str) -> str:
    return text.split('_')[0] + "".join(x.title() for x in text.split('_')[1:])


def camel_to_pascal(text: str) -> str:
    return text[0].upper() + text[1:]


def question(choices: EnumType) -> questionary.Question:
    prompt = camel_to_snake(choices.__name__).replace("_", " ")  # type: ignore
    return questionary.select(f"Select the {prompt}: ", choices=list(choices))


def binary_question(option: str) -> questionary.Question:
    return questionary.confirm(f"Do you want {option}?", default=False)


def text_question(default: str) -> questionary.Question:
    return questionary.text(f"The name of the database you want to create? ", default=default)
