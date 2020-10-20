import uuid
from datetime import datetime
from typing import List, Tuple, Optional

from django.db import models, connection
from django.db.models import Func

from core.note import Note
from common.db_functions import TsStatModel


class NoteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=11, editable=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def to_note(self):
        return Note(self.id, self.user_id, self.text, self.created_at)

    @classmethod
    def top_used_words(cls, from_date: Optional[datetime], to_date: Optional[datetime], n: int = 1) -> List[Tuple[str, int]]:
        query = NoteModel.objects.annotate(tsv=Func('text', function='to_tsvector'))
        if from_date is not None and to_date is not None:
            query = query.filter(created_at__range=(from_date, to_date))
        elif from_date is not None:
            query = query.filter(created_at__gt=from_date)
        elif to_date is not None:
            query = query.filter(created_at__lt=to_date)
        else:
            # no filtration required
            pass

        query_str = query.values('tsv')

        (query, params) = query_str.query.sql_with_params()
        cursor = connection.cursor()
        str_query = cursor.mogrify(query, params).decode()
        print(f'Ts vector query: <{str_query}>')

        res = TsStatModel\
            .objects\
            .all()\
            .table_function(query=str_query)\
            .order_by('-nentry', '-ndoc')[:n]\
            .values('word', 'nentry')
        print(f'Query ts stat: {res.query}')
        return list(map(lambda r: (r['word'], r['nentry']), res))
