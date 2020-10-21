from django.urls import path, re_path

from notekeeper.admin_view import get_notes_number_per_period, get_top_used_words_per_period

urlpatterns = [
    re_path(r'stats/notes-number/(?P<user_id>\w+)?$', get_notes_number_per_period, name='notes_number'),
    path('stats/top-used-words', get_top_used_words_per_period, name='top_used_words'),
]
