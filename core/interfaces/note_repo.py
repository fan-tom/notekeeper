from abc import ABC, abstractmethod
from typing import List

from core.note import UserId, Note


class NoteRepo(ABC):
    @abstractmethod
    def create(self, user_id: UserId, note: str) -> Note:
        pass

    def get_last(self, user_id: UserId, n: int) -> List[Note]:
        pass
