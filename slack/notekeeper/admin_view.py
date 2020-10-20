from typing import Optional

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from core.note import UserId
from common.serializers import DateTimeRangeSerializer
from .models import NoteModel


@api_view()
def get_notes_number_per_period(request: Request, user_id: Optional[UserId] = None) -> Response:
    """
    Return how many notes were created within given period, optionally filtered by user
    :param user_id: optional user id to filter by

    Time range is passed by query string parameters from_time and to_time,
    """

    serializer = DateTimeRangeSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    from_date, to_date = serializer.validated_data.get('from_date'), serializer.validated_data.get('to_date')
    if from_date is None:
        notes_qs = NoteModel.objects.filter(created_at__lt=to_date)
    else:
        notes_qs = NoteModel.objects.filter(created_at__range=(from_date, to_date))
    if user_id is not None:
        notes_qs = notes_qs.filter(user_id=user_id)
    return Response(dict(notes_number=notes_qs.count()))


@api_view()
def get_top_used_words_per_period(request: Request) -> Response:
    serializer = DateTimeRangeSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    from_date, to_date = serializer.validated_data.get('from_date'), serializer.validated_data.get('to_date')
    n_str = request.query_params.get('n', 1)
    try:
        n = int(n_str)
    except ValueError:
        raise ValidationError(f'Invalid number of words: expected integer, found {n_str}')
    return Response(dict(top_used_words=NoteModel.top_used_words(from_date, to_date, n)))
