from typing import Optional

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from core.entities import UserId
from common.serializers import DateTimeRangeSerializer
from .models import NoteModel


# REVIEW M1ha:
#  1. Нет проверок доступа
#  2. Не задан список методов доступа. Я могу сделать тот же запрос через POST...
#  3. Не используются Generic-и и возможнсти rest-framework: пагинация, сериализаторы
#  4. Почему файл называется admin_view? views должны быть во views.py.
#    Никакой логики в выделении их в отдельный файл (тем более при отсутсвии в package других view) не вижу.


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

    # REVIEW M1ha: Это не QuerySet. Это мендежер. Тогда надо добавить .all()
    notes_qs = NoteModel.objects
    if user_id is not None:
        notes_qs = notes_qs.filter(user_id=user_id)

    # REVIEW M1ha: Тут было бы достаточно 2 последовательных if. range - синтаксический сахар. Зачем все усложнять?
    if from_date is not None and to_date is not None:
        notes_qs = notes_qs.filter(created_at__range=(from_date, to_date))
    elif from_date is not None:
        notes_qs = notes_qs.filter(created_at__gte=from_date)
    elif to_date is not None:
        notes_qs = notes_qs.filter(created_at__lte=to_date)
    return Response(dict(notes_number=notes_qs.count()))


@api_view()
def get_top_used_words_per_period(request: Request) -> Response:
    serializer = DateTimeRangeSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    from_date, to_date = serializer.validated_data.get('from_date'), serializer.validated_data.get('to_date')

    # REVIEW M1ha: Почему этот параметр не проходит через валидацию? Зачем собственный костыль?
    n_str = request.query_params.get('n', 1)
    try:
        n = int(n_str)
    except ValueError:
        raise ValidationError(f'Invalid number of words: expected integer, found {n_str}')

    # REVIEW M1ha: Дублирующийся код. Та же обработка была во view выше.
    query = NoteModel.objects
    if from_date is not None and to_date is not None:
        query = query.filter(created_at__range=(from_date, to_date))
    elif from_date is not None:
        query = query.filter(created_at__gt=from_date)
    elif to_date is not None:
        query = query.filter(created_at__lt=to_date)
    else:
        # no filtration required
        pass

    # REVIEW M1ha: Эффективность это хорошо. Но читабельность такой конструкции нулевая.
    #  Как минимум, нужно форматировать нагляднее.
    #  А еще лучше QuerySet вообще вынести в отдельную переменную, зачем все в куче?
    return Response(dict(top_used_words=map(lambda r: (r.word, r.nentry), query
                                            .top_used_words()
                                            .order_by('-nentry', 'word')[:n]
                                            )))
