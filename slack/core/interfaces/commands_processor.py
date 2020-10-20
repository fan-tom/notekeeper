from abc import abstractmethod, ABC
from typing import Iterable

from .command import Command


class CommandsProcessor(ABC):
    @abstractmethod
    def get_supported_commands(self) -> Iterable[Command]:
        pass
