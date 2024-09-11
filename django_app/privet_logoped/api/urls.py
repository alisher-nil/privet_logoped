from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommandsViewSet,
    TelegramAnswersViewSet,
    TelegramQueryViewSet,
    TelegramUserViewSet,
    TimezonesView,
    VKAnswersViewSet,
    VKQueryViewSet,
    VKUserViewSet,
)

app_name = "api"
telegram_router = DefaultRouter()
telegram_router.register(
    r"users",
    TelegramUserViewSet,
    basename="telegram_users",
)
telegram_router.register(
    "user_query",
    TelegramQueryViewSet,
    basename="telegram_user_query",
)
telegram_router.register(
    "answers",
    TelegramAnswersViewSet,
    basename="telegram_answers",
)
telegram_urlpatterns = telegram_router.urls


vk_router = DefaultRouter()
vk_router.register(
    r"users",
    VKUserViewSet,
    basename="vk_users",
)
vk_router.register(
    "user_query",
    VKQueryViewSet,
    basename="vk_user_query",
)
vk_router.register(
    "answers",
    VKAnswersViewSet,
    basename="vk_answers",
)

common_router = DefaultRouter()
common_router.register(
    "commands",
    CommandsViewSet,
    basename="menu_commands",
)

v1_urlpatterns = [
    path("common/", include(common_router.urls)),
    path("common/timezones/", TimezonesView.as_view()),
    path("telegram/", include(telegram_urlpatterns)),
    path("vk/", include(vk_router.urls)),
]

urlpatterns = [
    path("v1/", include(v1_urlpatterns)),
]
