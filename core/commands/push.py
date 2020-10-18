from abc import abstractmethod, ABC

from core.note import NoteId, UserId
from core.interfaces import AuthorizedCommand


class PushHandler(ABC):
    @abstractmethod
    def handle_push(self, command: 'Push') -> NoteId:
        pass


class Push(AuthorizedCommand[PushHandler]):
    name = 'push'
    note: str

    def __init__(self, user_id: UserId, note: str):
        super().__init__(user_id)
        self.note = note

    def handle(self, handler: PushHandler):
        handler.handle_push(self)
