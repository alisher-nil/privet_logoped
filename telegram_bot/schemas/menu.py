from typing import List, Literal

from constants import CHAT_MESSAGE_MAX_LENGTH
from pydantic import BaseModel, Field, RootModel


class Link(BaseModel):
    url: str = Field(
        ...,
        title="URL",
        description="Ссылка",
    )
    title: str = Field(
        ...,
        title="Заголовок",
        description="Заголовок ссылки",
    )
    order: int = Field(
        ...,
        title="Порядок",
        description="Порядок ссылки",
        ge=0,
    )


class Attachment(BaseModel):
    file: str = Field(
        ...,
        title="Файл",
        description="Путь до файла вложения",
    )
    title: str = Field(
        ...,
        title="Заголовок",
        description="Заголовок файла",
    )
    order: int = Field(
        ...,
        title="Порядок",
        description="Порядок файла",
        ge=0,
    )


class MenuItem(BaseModel):
    id: int = Field(
        ...,
        title="ID",
        description="ID пункта меню",
    )
    title: str = Field(
        ...,
        title="Заголовок",
        description="Заголовок пункта меню",
    )
    order: int = Field(
        ...,
        title="Порядок",
        description="Порядок пункта меню",
        ge=0,
    )
    description: str = Field(
        ...,
        title="Описание",
        description="Описание пункта меню",
        max_length=CHAT_MESSAGE_MAX_LENGTH,
    )
    role: Literal["parent", "logoped"] = Field(
        ...,
        title="Роль",
        description="Роль пользователя",
    )
    links: list[Link] = Field([], title="Ссылки")
    attachments: list[Attachment] = Field([], title="Вложения")


CommandList = RootModel[List[MenuItem]]
