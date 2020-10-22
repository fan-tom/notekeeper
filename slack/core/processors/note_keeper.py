from typing import Tuple, Type, List

from core.entities import Note
from core.commands import Push, Top, PushHandler, TopHandler
from core.interfaces import NoteRepo, CommandsProcessor


class NoteKeeper(CommandsProcessor, PushHandler, TopHandler):
    """
    Can create and list last stored notes
    """
    repo: NoteRepo

    def __init__(self, repo: NoteRepo):
        self.repo = repo

    def get_supported_commands(self) -> Tuple[Type[Push], Type[Top]]:
        return Push, Top

    def handle_push(self, command: Push) -> Note:
        return self.repo.create(command.user_id, command.text)

    def handle_top(self, command: Top) -> List[Note]:
        return self.repo.get_last(command.user_id, command.n)
