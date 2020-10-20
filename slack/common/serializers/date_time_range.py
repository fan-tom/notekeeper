import datetime

from rest_framework import serializers


class DateTimeRangeSerializer(serializers.Serializer):
    from_date = serializers.DateTimeField(required=False)
    to_date = serializers.DateTimeField(default=datetime.datetime.now())
