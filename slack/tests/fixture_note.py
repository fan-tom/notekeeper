from datetime import datetime


class FixtureNote:
    user_id: str
    text: str
    created_at: datetime

    def __init__(self, user_id: str, text: str, created_at: int):
        self.user_id = user_id
        self.text = text
        self.created_at = datetime.utcfromtimestamp(created_at)
