import uuid

from django.db import models, connection
from django.db.models import Func, QuerySet
from django.utils import timezone

from core.entities import Note
from common.models import TsStatModel


class NoteQuerySet(models.QuerySet):
    def top_used_words(self) -> QuerySet[TsStatModel]:
        query = self.annotate(tsv=Func('text', function='to_tsvector'))

        query_str = query.values('tsv')

        (query, params) = query_str.query.sql_with_params()
        cursor = connection.cursor()
        str_query = cursor.mogrify(query, params).decode()
        print(f'Ts vector query: <{str_query}>')

        return TsStatModel.objects.all().table_function(query=str_query)


class NoteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=128, editable=False)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    objects = NoteQuerySet.as_manager()

    def to_note(self):
        return Note(self.id, self.user_id, self.text, self.created_at)
