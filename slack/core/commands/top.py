from abc import ABC, abstractmethod
from typing import Optional, List

from core.entities.note import UserId, Note
from core.interfaces import IdentifiedCommand


class TopHandler(ABC):
    """
    Top command executor interface
    """

    @abstractmethod
    def handle_top(self, command: 'Top') -> List[Note]:
        pass


class Top(IdentifiedCommand[TopHandler]):
    """Get n last notes (one if limit not specified)"""

    # REVIEW M1ha: Есть разница между переменными класса и переменными инстанса, задваемых через self.
    #  На int это не скажется, а на ссылочных структурах (словарях и списках) может запросто.
    n: int  # List limit

    def __init__(self, user_id: UserId, n: Optional[int]):
        super().__init__(user_id)

        # REVIEW M1ha: обычно это пишется как self.n = n or 1
        self.n = 1 if n is None else n

    def handle(self, handler: TopHandler) -> List[Note]:
        return handler.handle_top(self)
