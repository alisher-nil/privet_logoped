from django.conf import settings
from django.db import models

from bot_users.models import UserRoles
from privet_logoped.constants import (
    CHOISE_FIELD_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    URL_MAX_LENGTH,
)

attachments_dir = settings.ATTACHMENTS_DIR


class CommandItem(models.Model):
    title = models.CharField(
        "Заголовок",
        max_length=TITLE_MAX_LENGTH,
        help_text="Заголовок будет использоваться в качестве текста кнопки",
    )
    is_active = models.BooleanField("Активно", default=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        abstract = True
        ordering = ("order",)

    def __str__(self) -> str:
        return self.title


class MainMenuCommand(CommandItem):
    description = models.TextField(
        "Описание",
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
        help_text="Описание будет использоваться в тексте команды",
    )
    role = models.CharField(
        "Роль",
        max_length=CHOISE_FIELD_MAX_LENGTH,
        choices=UserRoles.choices,
    )

    class Meta:
        verbose_name = "Настраиваемый пункт меню"
        verbose_name_plural = "Настраиваемые пункты меню"

    def get_inline_title(self):
        return "Custom title"


class URLLink(CommandItem):
    url = models.URLField("Ссылка", max_length=URL_MAX_LENGTH)
    parent = models.ForeignKey(
        MainMenuCommand,
        on_delete=models.CASCADE,
        related_name="links",
    )

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"


class FileAttachment(CommandItem):
    file = models.FileField("Файл", upload_to=attachments_dir)
    parent = models.ForeignKey(
        MainMenuCommand,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
