from typing import Tuple, Type, List

from core.entities import Note
from core.commands import Push, Top, PushHandler, TopHandler
from core.interfaces import NoteRepo, CommandsProcessor


# REVIEW M1ha: Смешались вместе кони, люди. Какой-то гаврик на верблюде...
#  Почему оно наследутеся от CommandProcessor и от каких-то левых Handler-ов?
#  Что вообще представляет этот класс? Если команд будет 10? 20? 1000?
#  Гораздо проще было бы, реализуй он только CommandProcessor.
#  Команды, реализующие интерфейс Command, лучше хранить где-то в атрибуте в словаре
#  При необходимости доставать команду по имени и вызывать у нее handle(...). Все.
#  -100500 лишних интерфейсов, +100500 к прозрачности кода.

# REVIEW M1ha: Кроме того, если core хранит интерфейсы, почему тут лежит реализация?
#  Логически это должно быть в notekeeper или common
#  (хотя на данный момент я так и не понял, зачем все это вообще делить на отдельыне package)

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
