from abc import abstractmethod, ABC

from .command import Command


class CommandsProcessor(ABC):
    @abstractmethod
    def get_supported_commands(self) -> Command:
        pass
