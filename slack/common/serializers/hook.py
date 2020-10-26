from rest_framework import serializers
from datetime import datetime


class TimestampField(serializers.DateTimeField):

    def to_internal_value(self, value):
        # REVIEW M1ha: Работа с timestamp это вобще отдельная тема. Если он приходит в utc, какая тут таймзона будет?
        #  Явно она не задана, скорее всего будет aware. Там есть тонкости.
        dt = datetime.fromtimestamp(float(value))
        return super().to_internal_value(dt)


class HookSerializer(serializers.Serializer):
    """
    NOTE M1ha: валидация вебхука от Slack
    REVIEW M1ha: Плюс за наличие валидации и использование механики валидации rest_framework.
    """
    token = serializers.CharField()  # snrQzbevYyXpBp8LA2q6hnuU
    team_id = serializers.RegexField(r'T\d+')  # T0001
    team_domain = serializers.CharField(required=False)  # example

    channel_id = serializers.RegexField(r'C\d+')  # C2147483705
    channel_name = serializers.CharField()  # test

    timestamp = TimestampField()  # 1355517523.000005
    user_id = serializers.RegexField(r'U\w+')  # U2147483697
    user_name = serializers.CharField()  # Steve

    text = serializers.CharField()  # googlebot: What is the air-speed velocity of an unladen swallow?

    trigger_word = serializers.CharField()  # googlebot:
