from datetime import datetime

# REVIEW M1ha: Почему не используется механизм fixture django? Зачем эти нестандартные костыли?
#  https://docs.djangoproject.com/en/3.1/howto/initial-data/

class FixtureNote:
    user_id: str
    text: str
    created_at: datetime

    def __init__(self, user_id: str, text: str, created_at: int):
        self.user_id = user_id
        self.text = text
        self.created_at = datetime.utcfromtimestamp(created_at)
