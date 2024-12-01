from rest_framework.serializers import ValidationError


def validate_youtube_link(value):
    if "youtube.com" not in value:
        raise ValidationError("можно постить только ссылки на ютуб")