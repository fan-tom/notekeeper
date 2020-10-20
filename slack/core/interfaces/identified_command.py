from abc import ABC
from typing import Generic

from core.note import UserId
from .command import Command, Handler


class IdentifiedCommand(Command[Handler], ABC, Generic[Handler]):
    user_id: UserId

    def __init__(self, user_id: UserId):
        self.user_id = user_id
