import json
from collections import defaultdict
from datetime import datetime
from typing import List, Optional

from django.test import TestCase, override_settings
from django.urls import reverse

from notekeeper.models import NoteModel
from .fixture_note import FixtureNote


@override_settings(DEBUG=True)
class AdminEndpointsTest(TestCase):
    notes: List[FixtureNote]

    @classmethod
    def setUpTestData(cls):
        # REVIEW M1ha: Почему не используется механизм fixture django? Зачем эти нестандартные костыли?
        #  https://docs.djangoproject.com/en/3.1/howto/initial-data/
        with open('tests/fixtures/notes.json') as fixture:
            content = fixture.read()
            notes = list(FixtureNote(**n) for n in json.loads(content))
        NoteModel.objects.bulk_create(
            (NoteModel(user_id=note.user_id, text=note.text, created_at=note.created_at) for note in notes))
        cls.notes = notes

    def filter_notes(self, user_id: Optional[str] = None, from_date: Optional[datetime] = None,
                     to_date: Optional[datetime] = None) -> List[FixtureNote]:
        res = self.notes
        if user_id is not None:
            res = list(n for n in res if n.user_id == user_id)
        if from_date is not None:
            res = list(n for n in res if n.created_at >= from_date)
        if to_date is not None:
            res = list(n for n in res if n.created_at <= to_date)
        return res

    def count_words(self, notes: List[FixtureNote]) -> List[List]:
        """
        Returns list of word counts, sorted descending
        (most used first, words with the same freq. are sorted lexicographically)
        """

        word_stat = defaultdict(int)
        for note in notes:
            words = note.text.split()
            for word in words:
                word_stat[word] += 1
        count_to_words = defaultdict(list)
        for k, v in word_stat.items():
            count_to_words[v].append(k)
        sorted_words = ((count, sorted(words)) for (count, words) in count_to_words.items())
        sorted_counts = sorted(sorted_words, key=lambda n: n[0], reverse=True)
        return list([word, count] for (count, words) in sorted_counts for word in words)

    def test_get_notes_number_per_period_without_filter(self):
        response = self.client.get(reverse('notes_number'))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["notes_number"], len(self.notes))

    def test_get_notes_number_per_period_by_user_only(self):
        user_id = self.notes[0].user_id
        expected = sum(1 for _ in self.filter_notes(user_id))
        response = self.client.get(reverse('notes_number', args=[user_id]))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["notes_number"], expected)

    def test_get_notes_number_per_period_by_user_and_start_time(self):
        user_id = self.notes[0].user_id
        from_date = self.notes[0].created_at
        expected = sum(1 for _ in self.filter_notes(user_id, from_date))
        response = self.client.get(reverse('notes_number', args=[user_id]), data=dict(from_date={from_date.isoformat()}))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["notes_number"], expected)

    def test_get_notes_number_per_period_by_user_and_end_time(self):
        user_id = self.notes[0].user_id
        to_date = sorted(self.filter_notes(user_id), key=lambda n: n.created_at)[-1].created_at
        expected = sum(1 for _ in self.filter_notes(user_id, None, to_date))
        response = self.client.get(reverse('notes_number', args=[user_id]), data=dict(to_date={to_date.isoformat()}))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["notes_number"], expected)

    def test_get_top_used_words_without_filters(self):
        expected = self.count_words(self.notes)[:1]
        response = self.client.get(reverse('top_used_words'))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["top_used_words"], expected)

    def test_get_top_used_words_limiting_number(self):
        n = 4
        expected = self.count_words(self.notes)[:4]
        response = self.client.get(reverse('top_used_words'), data=dict(n=n))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["top_used_words"], expected)

    def test_get_top_used_words_limiting_period(self):
        dates = sorted(set(n.created_at for n in self.notes))
        from_date = dates[1]
        to_date = dates[-2]
        expected = self.count_words(self.filter_notes(from_date=from_date, to_date=to_date))[:1]
        response = self.client.get(reverse('top_used_words'), data=dict(from_date=from_date.isoformat(), to_date=to_date.isoformat()))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["top_used_words"], expected)
