from abc import abstractmethod, ABC
from typing import TypeVar, Generic, ClassVar

Handler = TypeVar('Handler')


class Command(ABC, Generic[Handler]):
    name: ClassVar[str]

    @abstractmethod
    def handle(self, handler: Handler):
        pass
