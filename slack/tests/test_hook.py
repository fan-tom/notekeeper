import json
import re
from datetime import datetime
from typing import Optional, List

from django.test import override_settings, TestCase
from rest_framework.test import APITestCase

from notekeeper.models import NoteModel
from tests.fixture_note import FixtureNote
from tests.urlencoded_renderer import UrlencodedRenderer

SLACK_TOKEN = 'slack_token'

@override_settings(DEBUG=True, SLACK_TOKEN=SLACK_TOKEN)
class HookTest(APITestCase):
    notes: List[FixtureNote]

    @classmethod
    def setUpTestData(cls):
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

    def call_hook(self, user_id: str, text: str):
        return self.client.post(
            '/slackhook/',
            # content_type="application/x-www-form-urlencoded",
            data=dict(
                    token=SLACK_TOKEN,
                    team_id='T0',
                    channel_id='C0',
                    channel_name='test',
                    timestamp=datetime.now().timestamp(),
                    user_id=user_id,
                    user_name='test_user',
                    text=text,
                    trigger_word='notekeeper'
                ),
            format=UrlencodedRenderer.format,
        )

    def test_push(self):
        text = 'notekeeper push my note'
        response = self.call_hook('Utest_user_1', text)
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.json()['text'], 'Note was saved with id .*')

    def test_top_without_number(self):
        response = self.call_hook('Utest_user_1', 'notekeeper push my note 1')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.json()['text'], 'Note was saved with id .*')

        note_2 = 'my note 2'
        response = self.call_hook('Utest_user_1', f'notekeeper push {note_2}')
        self.assertEqual(response.status_code, 200)
        text = response.json()['text']
        message_id_re = re.compile(r'Note was saved with id (.*)')
        self.assertRegex(text, message_id_re)
        message_id = message_id_re.match(text).group(1)

        response = self.call_hook('Utest_user_1', 'notekeeper top')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.json()['text'], f"""Last note:\n\nId: {message_id}\nCreated at: .*\nText: {note_2}""")

    def test_top_with_number(self):
        response = self.call_hook('Utest_user_1', 'notekeeper push my note 1')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.json()['text'], 'Note was saved with id .*')

        message_id_re = re.compile(r'Note was saved with id (.*)')

        note_2 = 'my note 2'
        response = self.call_hook('Utest_user_1', f'notekeeper push {note_2}')
        self.assertEqual(response.status_code, 200)
        text = response.json()['text']
        self.assertRegex(text, message_id_re)
        message_id_2 = message_id_re.match(text).group(1)

        note_3 = 'my note 3'
        response = self.call_hook('Utest_user_1', f'notekeeper push {note_3}')
        self.assertEqual(response.status_code, 200)
        text = response.json()['text']
        self.assertRegex(text, message_id_re)
        message_id_3 = message_id_re.match(text).group(1)

        response = self.call_hook('Utest_user_1', 'notekeeper top 2')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.json()['text'], fr"""Last 2 notes:

Id: {message_id_3}
Created at: .*
Text: {note_3}

Id: {message_id_2}
Created at: .*
Text: {note_2}""")

    def test_top_takes_user_id_into_account(self):
        message_id_re = re.compile(r'Note was saved with id (.*)')

        note_1 = 'my note 1'
        response = self.call_hook('Utest_user_1', f'notekeeper push {note_1}')
        self.assertEqual(response.status_code, 200)
        text = response.json()['text']
        self.assertRegex(text, message_id_re)
        message_id_1 = message_id_re.match(text).group(1)

        note_2 = 'my note 2'
        response = self.call_hook('Utest_user_2', f'notekeeper push {note_2}')
        self.assertEqual(response.status_code, 200)
        text = response.json()['text']
        self.assertRegex(text, message_id_re)

        note_3 = 'my note 3'
        response = self.call_hook('Utest_user_1', f'notekeeper push {note_3}')
        self.assertEqual(response.status_code, 200)
        text = response.json()['text']
        self.assertRegex(text, message_id_re)
        message_id_3 = message_id_re.match(text).group(1)

        response = self.call_hook('Utest_user_1', 'notekeeper top 2')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.json()['text'], fr"""Last 2 notes:

Id: {message_id_3}
Created at: .*
Text: {note_3}

Id: {message_id_1}
Created at: .*
Text: {note_1}""")
