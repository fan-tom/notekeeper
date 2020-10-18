from core.Note import Note
from core.commands import Push, Top, PushHandler, TopHandler
from core.interfaces import NoteRepo, CommandsProcessor


class NoteKeeper(CommandsProcessor, PushHandler, TopHandler):
    repo: NoteRepo

    def __init__(self, repo: NoteRepo):
        self.repo = repo

    def get_supported_commands(self) -> str:  # Tuple[Type[Push], Type[Top]]:
        return ''  # Push, Top

    def handle_push(self, command: Push) -> Note:
        return self.repo.create(command.user_id, command.note)

    def handle_top(self, command: Top):
        return self.repo.get_last(command.user_id, command.n)
