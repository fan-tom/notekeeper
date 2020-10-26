from datetime import datetime
from typing import NewType
from uuid import UUID

# REVIEW M1ha: Мне непонятно, зачем переименовывать терминальные типы. Я понимаю структуры/классы.
#  Но обилие избыточных ссылок только усложняет восприятие и не несут полезной нагрузки.
NoteId = NewType('NoteId', UUID)
UserId = NewType('UserId', str)

class Note:
    """
    Class, that represents saved note, belonging to some user

    Attributes
    ----------
    id: note identifier
    user_id: identifier of user, this note belongs to
    text: note content
    created_at: when note was created

    REVIEW M1ha: Я бы просто совместил это с моделью NoteModel.
      Это достаточное описание и никаких доп. интерфейсов / wrapper-ов не нужно.
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
