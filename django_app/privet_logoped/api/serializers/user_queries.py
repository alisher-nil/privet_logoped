from rest_framework import serializers

from bot_users.models import BotUser, TelegramUser, VKUser
from user_queries.models import QueryAnswer, UserQuery


class QueryReadSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(
        source="bot_user", read_only=True, slug_field="user_id"
    )

    class Meta:
        model = UserQuery
        fields = ["id", "user_id", "question_text", "message_id", "created_at"]


class UserQueryWriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        bot_user_model: BotUser
        model = UserQuery
        fields = [
            "user_id",
            "question_text",
            "message_id",
        ]

    def validate_user_id(self, value: int):
        if not self.Meta.bot_user_model.objects.filter(user_id=value).exists():
            raise serializers.ValidationError(
                "User with this user_id does not exist"
            )
        return value

    def to_internal_value(self, data: dict):
        validated_data = super().to_internal_value(data)
        user_id = validated_data.pop("user_id")
        user = self.Meta.bot_user_model.objects.get(user_id=user_id)
        validated_data["bot_user"] = user
        validated_data["role"] = user.role
        return validated_data

    def to_representation(self, instance: UserQuery):
        return QueryReadSerializer(instance).data


class TelegramQueryWriteSerializer(UserQueryWriteSerializer):
    class Meta:
        bot_user_model = TelegramUser
        model = UserQuery
        fields = [
            "user_id",
            "question_text",
            "message_id",
        ]


class VKQueryWriteSerializer(UserQueryWriteSerializer):
    class Meta:
        bot_user_model = VKUser
        model = UserQuery
        fields = [
            "user_id",
            "question_text",
            "message_id",
        ]


class AnswerReadSerializer(serializers.ModelSerializer):
    user_query = QueryReadSerializer()

    class Meta:
        model = QueryAnswer
        fields = ["id", "answer_text", "created_at", "user_query"]


class IdListSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )

    class Meta:
        fields = ["ids"]

    def validate_ids(self, value):
        queryset = self.context["view"].get_queryset().filter(id__in=value)
        if not queryset.exists():
            raise serializers.ValidationError("No valid objects found")
        return value
