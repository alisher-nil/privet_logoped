from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from bot_users.models import UserRoles
from privet_logoped.constants import (
    CHOISE_FIELD_MAX_LENGTH,
    MESSAGE_MAX_LENGTH,
)

User = get_user_model()


class UserQuery(models.Model):
    ALLOWED_MODELS = ["telegramuser", "vkuser"]

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ALLOWED_MODELS},
    )
    object_id = models.PositiveIntegerField()
    bot_user = GenericForeignKey("content_type", "object_id")
    role = models.CharField(
        max_length=CHOISE_FIELD_MAX_LENGTH,
        choices=UserRoles.choices,
    )
    question_text = models.TextField(max_length=MESSAGE_MAX_LENGTH)
    message_id = models.PositiveBigIntegerField("ID сообщения", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Вопрос пользователя"
        verbose_name_plural = "Вопросы пользователей"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"Вопрос от {self.bot_user} от {self.created_at}"


class QueryAnswer(models.Model):
    user_query = models.ForeignKey(
        UserQuery,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    answer_text = models.TextField(max_length=MESSAGE_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"
