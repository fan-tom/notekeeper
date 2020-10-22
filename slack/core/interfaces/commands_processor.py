from abc import abstractmethod, ABC
from typing import Iterable, Type

from .command import Command


class CommandsProcessor(ABC):
    """Base class for commands processors"""

    @abstractmethod
    def get_supported_commands(self) -> Iterable[Type[Command]]:
        """Returns classes of commands, supported by this processor"""
        pass
