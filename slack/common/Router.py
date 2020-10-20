from typing import Dict, Optional, Type, Iterable

from core.interfaces import CommandsProcessor, Command


class Router:
    bots: Dict[str, CommandsProcessor]
    commands: Dict[str, Type[Command]]

    def __init__(self, bots: Dict[str, CommandsProcessor], commands: Dict[str, Type[Command]]):
        self.bots = bots
        self.commands = commands

    def get_bot(self, bot_name: str) -> Optional[CommandsProcessor]:
        return self.bots.get(bot_name)

    def get_command_class(self, cmd_name) -> Optional[Type[Command]]:
        return self.commands.get(cmd_name)

    def get_command_names(self, commands: Iterable[Type[Command]]) -> Dict[Type[Command], Optional[str]]:
        return dict(map(lambda c: (c, next((key for key, value in self.commands.items() if value == c), None)), commands))

    def get_bot_names(self) -> Iterable[str]:
        return self.bots.keys()
