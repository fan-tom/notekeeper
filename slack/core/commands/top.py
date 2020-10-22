from abc import ABC, abstractmethod
from typing import Optional, List

from core.entities.note import UserId, Note
from core.interfaces import IdentifiedCommand


class TopHandler(ABC):
    @abstractmethod
    def handle_top(self, command: 'Top') -> List[Note]:
        pass


class Top(IdentifiedCommand[TopHandler]):
    """
    Get n last notes (one if limit not specified)
    """
    name = 'top'
    n: int

    def __init__(self, user_id: UserId, n: Optional[int]):
        super().__init__(user_id)
        self.n = 1 if n is None else n

    def handle(self, handler: TopHandler) -> List[Note]:
        return handler.handle_top(self)
