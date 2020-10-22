from abc import ABC
from typing import TypeVar

from core.entities import UserId
from core.interfaces import IdentifiedCommand
from .command_wrapper import CommandWrapper, O

C = TypeVar('C', bound=IdentifiedCommand)


class IdentifiedCommandWrapper(CommandWrapper[C, O], ABC):
    """Base class for deserialized of commands, that require user id"""

    user_id: UserId

    def __init__(self, user_id: UserId):
        """
        :param user_id: user id, required to create Push command
        """
        super().__init__()
        self.user_id = user_id
