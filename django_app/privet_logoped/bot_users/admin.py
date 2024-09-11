from django.contrib.admin import register
from unfold.admin import ModelAdmin

from bot_users.models import TelegramUser, VKUser


@register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ("user_id", "role")
    list_filter = ("role",)


@register(VKUser)
class VKUserAdmin(ModelAdmin):
    list_display = ("user_id", "role")
    list_filter = ("role",)
