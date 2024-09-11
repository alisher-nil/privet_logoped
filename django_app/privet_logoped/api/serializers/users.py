from rest_framework import serializers

from bot_users.models import TelegramUser, UserRoles, UserTimezone, VKUser


class BotUserSerializer(serializers.ModelSerializer):
    def validate_role(self, value):
        if value not in UserRoles.values:
            raise serializers.ValidationError("Invalid role")
        return value

    def validate_timezone(self, value):
        if value not in UserTimezone.values:
            raise serializers.ValidationError("Invalid timezone")
        return value


class TelegramUserSerializer(BotUserSerializer):
    class Meta:
        model = TelegramUser
        fields = ["user_id", "role", "timezone"]


class TelegramUserUpdateSerializer(TelegramUserSerializer):
    user_id = serializers.IntegerField(read_only=True)


class VKUserSerializer(BotUserSerializer):
    timezone = serializers.CharField(required=False)

    class Meta:
        model = VKUser
        fields = ["user_id", "role", "timezone"]


class VKUserUpdateSerializer(VKUserSerializer):
    user_id = serializers.IntegerField(read_only=True)
