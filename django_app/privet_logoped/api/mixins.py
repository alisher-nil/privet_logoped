from django.db import DatabaseError
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.user_queries import AnswerReadSerializer, IdListSerializer
from user_queries.models import QueryAnswer


class CreateUpdateRetrieveMixin(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    pass


class BotUserViewSetMixin(CreateUpdateRetrieveMixin):
    update_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return self.update_serializer_class
        return super().get_serializer_class()


class ListViewSetMixin(ListModelMixin, GenericViewSet):
    pass


class CreateViewSetMixin(CreateModelMixin, GenericViewSet):
    pass


class AnswerViewSetMixin(ListViewSetMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = AnswerReadSerializer
    model = QueryAnswer
    user_content_type = None

    def get_queryset(self):
        queryset = (
            QueryAnswer.objects.filter(
                user_query__content_type=self.user_content_type,
                sent=False,
            )
            .select_related("user_query")
            .prefetch_related("user_query__bot_user")
        )
        return queryset

    @action(["post"], detail=False)
    def confirm_sent(self, request, *args, **kwargs):
        serializer = IdListSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset().filter(
            id__in=serializer.validated_data["ids"]
        )
        try:
            count = queryset.update(sent=True)
        except DatabaseError:
            return Response("Database error", status=500)

        return Response({"detail": f"Updated {count} objects"}, status=200)
