from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

# from django.db import models
# from unfold.decorators import action
# from unfold.contrib.forms.widgets import WysiwygWidget

admin.site.unregister(User)
admin.site.unregister(Group)


@register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = [
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
        "display_created",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {
                "fields": (("first_name", "last_name"), "email"),
                "classes": ["tab"],
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ["tab"],
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    # formfield_overrides = {
    #     models.TextField: {
    #         "widget": WysiwygWidget,
    #     }
    # }
    readonly_fields = ["last_login", "date_joined"]

    @display(description="Пользователь")
    def display_header(self, instance: User):
        return instance.username

    @display(description="Сотрудник", boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description="Суперпользователь", boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description="Дата создания")
    def display_created(self, instance: User):
        return instance.date_joined


@register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
