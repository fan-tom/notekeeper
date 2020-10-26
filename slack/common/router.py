from typing import Dict, Optional, Type, Iterable

from core.entities import UserId
from core.interfaces import CommandsProcessor, Command
from notekeeper.commands_deserializers import IdentifiedCommandWrapper


class Router:
    """Maps botnames and command names to bots and commands"""

    processors: Dict[str, CommandsProcessor]
    command_wrappers: Dict[str, Type[IdentifiedCommandWrapper]]

    def __init__(self, bots: Dict[str, CommandsProcessor], commands: Dict[str, Type[IdentifiedCommandWrapper]]):
        self.processors = bots
        self.command_wrappers = commands

    def get_bot(self, bot_name: str) -> Optional[CommandsProcessor]:
        return self.processors.get(bot_name)

    def get_command_class(self, cmd_name) -> Optional[Type[Command]]:
        wrapper = self.command_wrappers.get(cmd_name)
        if wrapper is None:
            return None
        else:
            return wrapper.command_class

    def get_command_names(self, commands: Iterable[Type[Command]]) -> Dict[Type[Command], Optional[str]]:
        # REVIEW M1ha: неэффективно
        #  Сложная структура wrapper-ов привела к тому, что сложно искать.
        #  Будь там обычный словарь по имени команды, было бы в разы проще.
        return dict((c, next((key for key, value in self.command_wrappers.items() if value.command_class == c), None))
                    for c in commands)

    def get_bot_names(self) -> Iterable[str]:
        return self.processors.keys()

    def create_wrapper(self, cmd_name: str, user_id: UserId) -> Optional[IdentifiedCommandWrapper]:
        wrapper_class = self.command_wrappers.get(cmd_name)
        if wrapper_class is None:
            return None
        else:
            return wrapper_class(user_id)
