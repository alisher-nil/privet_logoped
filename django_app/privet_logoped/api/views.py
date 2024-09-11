from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import (
    AnswerViewSetMixin,
    BotUserViewSetMixin,
    CreateViewSetMixin,
    ListViewSetMixin,
)
from api.serializers.command_content import CommandsSerializer
from api.serializers.user_queries import (
    TelegramQueryWriteSerializer,
    VKQueryWriteSerializer,
)
from api.serializers.users import (
    TelegramUserSerializer,
    TelegramUserUpdateSerializer,
    VKUserSerializer,
    VKUserUpdateSerializer,
)
from bot_users.models import TelegramUser, UserTimezone, VKUser
from commands.models import FileAttachment, MainMenuCommand, URLLink
from user_queries.models import UserQuery


class CommandsViewSet(ListViewSetMixin):
    permission_classes = [permissions.AllowAny]
    model = MainMenuCommand
    serializer_class = CommandsSerializer

    def get_queryset(self):
        links = URLLink.objects.filter(is_active=True)
        attachments = FileAttachment.objects.filter(is_active=True)
        return MainMenuCommand.objects.filter(is_active=True).prefetch_related(
            Prefetch("links", queryset=links),
            Prefetch("attachments", queryset=attachments),
        )


class TimezonesView(APIView):
    def get(self, requset):
        timezones = [
            {"timezone": timezone, "label": label}
            for timezone, label in UserTimezone.choices
        ]
        return Response(timezones)


class TelegramUserViewSet(BotUserViewSetMixin):
    permission_classes = [permissions.AllowAny]
    model = TelegramUser
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    update_serializer_class = TelegramUserUpdateSerializer
    lookup_field = "user_id"


class VKUserViewSet(BotUserViewSetMixin):
    permission_classes = [permissions.AllowAny]
    model = VKUser
    queryset = VKUser.objects.all()
    serializer_class = VKUserSerializer
    update_serializer_class = VKUserUpdateSerializer
    lookup_field = "user_id"


class TelegramQueryViewSet(CreateViewSetMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = TelegramQueryWriteSerializer
    model = UserQuery


class VKQueryViewSet(CreateViewSetMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = VKQueryWriteSerializer
    model = UserQuery


class TelegramAnswersViewSet(AnswerViewSetMixin):
    def initial(self, request, *args, **kwargs):
        self.user_content_type = ContentType.objects.get_for_model(
            TelegramUser
        )
        return super().initial(request, *args, **kwargs)


class VKAnswersViewSet(AnswerViewSetMixin):
    def initial(self, request, *args, **kwargs):
        self.user_content_type = ContentType.objects.get_for_model(VKUser)
        return super().initial(request, *args, **kwargs)
