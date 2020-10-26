from abc import abstractmethod, ABC
from typing import TypeVar, Generic

Handler = TypeVar('Handler')


# REVIEW M1ha: Ну ок. Еще один малозначимый интерфейс. А почему это лежит не в core.commands?

class Command(ABC, Generic[Handler]):
    """Base command class"""

    @abstractmethod
    def handle(self, handler: Handler):
        """
        Uses handler's methods to execute itself
        Return type depends on Handler
        """
        pass
