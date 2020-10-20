from abc import ABC, abstractmethod
from typing import List

from core.note import UserId, Note


class NoteRepo(ABC):
    """
    Note repository interface
    """
    @abstractmethod
    def create(self, user_id: UserId, text: str) -> Note:
        """
        Create Note with given text, bound to given user
        :param user_id: user note is bound to
        :param text: note text
        :return: Note object (fills id and created_at properties)
        """
        pass

    @abstractmethod
    def get_last(self, user_id: UserId, n: int) -> List[Note]:
        """
        Returns last n notes, created by given user
        :param user_id: user notes must be bound to
        :param n: how many notes to return (upper limit, may return less)
        :return: list of no more than n notes, created by given user
        """
        pass
