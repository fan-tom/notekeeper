from collections import OrderedDict

from django.db import models
from .table_functions.table_function import TableFunctionArg, TableFunctionManager


class TsStatModel(models.Model):
    """
    Model for ts_stat table function output
    See https://postgrespro.ru/docs/postgrespro/9.6/textsearch-features#textsearch-statistics
    """
    function_args = OrderedDict((
        ('query', TableFunctionArg()),
        ('wights', TableFunctionArg(required=False)),
    ))

    objects = TableFunctionManager()

    word = models.CharField(primary_key=True, max_length=128)
    ndoc = models.PositiveIntegerField()
    nentry = models.PositiveIntegerField()

    class Meta:
        db_table = 'ts_stat'
        managed = False

    def __str__(self):
        return self.word
