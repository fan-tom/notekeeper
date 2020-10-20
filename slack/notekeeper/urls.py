from django.urls import path, re_path

from notekeeper.admin_view import get_notes_number_per_period, get_top_used_words_per_period

urlpatterns = [
    re_path(r'stats/notes-per-period/(?P<user_id>U\d{11})?$', get_notes_number_per_period),
    path('stats/top-used-words', get_top_used_words_per_period),
]
