from datetime import datetime
from typing import NewType
from uuid import UUID

NoteId = NewType('NoteId', UUID)
UserId = NewType('UserId', UUID)


class Note:
    """
    Class, that represents saved note, belonging to some user
    Attributes
    ----------
    id: note identifier
    user_id: identifier of user, this note belongs to
    text: note content
    created_at: when note was created
    """

    id: NoteId
    user_id: UserId
    text: str
    created_at: datetime

    def __init__(self, id: NoteId, user_id: UserId, text: str, created_at: datetime):
        self.id = id
        self.user_id = user_id
        self.text = text
        self.created_at = created_at
