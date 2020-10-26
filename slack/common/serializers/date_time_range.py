import datetime

from rest_framework import serializers


class DateTimeRangeSerializer(serializers.Serializer):
    from_date = serializers.DateTimeField(required=False)

    # REVIEW M1ha: datetime.datetime.now() не учитывает TZ_INFO и TIME_ZONE из настроек django
    #  Надо использовать django.utils.timezone.now()
    to_date = serializers.DateTimeField(default=datetime.datetime.now())
