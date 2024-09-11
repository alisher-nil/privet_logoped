from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from user_queries.models import QueryAnswer, UserQuery


@admin.register(QueryAnswer)
class QueryAnswerAdmin(ModelAdmin):
    list_display = (
        "id",
        "user_query",
        "answer_text",
        "created_at",
        "author",
        "sent",
    )
    list_editable = ("sent",)


class AnswersInline(TabularInline):
    model = QueryAnswer
    extra = 0


@admin.register(UserQuery)
class UserQueryAdmin(ModelAdmin):
    list_display = (
        "id",
        "bot_user",
        "role",
        "question_text",
        "created_at",
    )
    readonly_fields = (
        "content_type",
        "object_id",
        "message_id",
        "question_text",
        "created_at",
        "role",
    )
    fieldsets = (
        (
            None,
            {"fields": ("role",), "classes": ("tab",)},
        ),
        (
            "Текст вопроса",
            {"fields": ("question_text",), "classes": ("tab",)},
        ),
        (
            "Дополнительно",
            {"fields": ("message_id", "created_at"), "classes": ("tab",)},
        ),
    )
    inlines = [AnswersInline]
