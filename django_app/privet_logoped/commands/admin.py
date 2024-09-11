from django.conf import settings
from django.contrib.admin import register
from unfold.admin import ModelAdmin, TabularInline

from .models import FileAttachment, MainMenuCommand, URLLink

base_dir = settings.BASE_DIR


class URLLinkInline(TabularInline):
    model = URLLink
    extra = 0
    fields = ("url", "title", "is_active", "order")


class FileAttachmentInline(TabularInline):
    model = FileAttachment
    extra = 0
    fields = ("file", "title", "is_active", "order")


@register(MainMenuCommand)
class MainMenuCommandsAdmin(ModelAdmin):
    fieldsets = (
        (
            "Заголовок и описание",
            {
                "fields": ("title", "description"),
                "classes": ["tab"],
            },
        ),
        (
            "Настройки",
            {
                "fields": ("is_active", "order", "role"),
                "classes": ["tab"],
            },
        ),
    )
    list_display = ("title", "role", "is_active", "order")
    inlines = [URLLinkInline, FileAttachmentInline]
    list_editable = ("is_active", "order", "role")
    list_filter = ("role", "is_active")
    ordering = ("order",)
