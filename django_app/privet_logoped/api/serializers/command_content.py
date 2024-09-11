from rest_framework import serializers

from commands.models import (
    FileAttachment,
    MainMenuCommand,
    URLLink,
)


class URLLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLLink
        fields = ["url", "title", "order"]


class FileAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)

    class Meta:
        model = FileAttachment
        fields = ["file", "title", "order"]


class CommandsSerializer(serializers.ModelSerializer):
    links = URLLinkSerializer(many=True)
    attachments = FileAttachmentSerializer(many=True)

    class Meta:
        model = MainMenuCommand
        fields = [
            "id",
            "title",
            "order",
            "description",
            "role",
            "links",
            "attachments",
        ]
