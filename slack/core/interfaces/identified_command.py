from abc import ABC
from typing import Generic

from core.entities import UserId
from .command import Command, Handler


class IdentifiedCommand(Command[Handler], ABC, Generic[Handler]):
    """Base class for commands, that require user id"""

    user_id: UserId  # id of user this command is executed on behalf of

    def __init__(self, user_id: UserId):
        self.user_id = user_id
