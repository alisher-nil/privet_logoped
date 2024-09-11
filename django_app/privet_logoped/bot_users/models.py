from django.db import models

from privet_logoped.constants import CHOISE_FIELD_MAX_LENGTH


class UserRoles(models.TextChoices):
    PARENT = "parent", "родитель"
    LOGOPED = "logoped", "логопед"


class UserTimezone(models.TextChoices):
    Kaliningrad = "Europe/Kaliningrad", "Калининградское (UTC+2)"
    Moscow = "Europe/Moscow", "Московское (UTC+3)"
    Samara = "Europe/Samara", "Самарское (UTC+4)"
    Yekaterinburg = "Asia/Yekaterinburg", "Екатеринбургское (UTC+5)"
    Omsk = "Asia/Omsk", "Омское (UTC+6)"
    Krasnoyarsk = "Asia/Krasnoyarsk", "Красноярское (UTC+7)"
    Irkutsk = "Asia/Irkutsk", "Иркутское (UTC+8)"
    Yakutsk = "Asia/Yakutsk", "Якутское (UTC+9)"
    Vladivostok = "Asia/Vladivostok", "Владивостокское (UTC+10)"
    Magadan = "Asia/Magadan", "Магаданское (UTC+11)"
    Kamchatka = "Asia/Kamchatka", "Камчатское (UTC+12)"


class BotUser(models.Model):
    user_id = models.BigIntegerField("ID пользователя", unique=True)
    role = models.CharField(
        max_length=CHOISE_FIELD_MAX_LENGTH,
        choices=UserRoles.choices,
    )
    timezone = models.CharField(
        max_length=CHOISE_FIELD_MAX_LENGTH,
        choices=UserTimezone.choices,
        default=UserTimezone.Moscow,
    )

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["user_id"])]


class TelegramUser(BotUser):
    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        return f"пользователь Telegram {self.user_id}"


class VKUser(BotUser):
    class Meta:
        verbose_name = "Пользователь VK"
        verbose_name_plural = "Пользователи VK"

    def __str__(self):
        return f"пользователь ВК {self.user_id}"
