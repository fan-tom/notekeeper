from abc import ABC
from typing import Generic

from core.Note import UserId
from .Command import Command, Handler


class AuthorizedCommand(ABC, Generic[Handler], Command[Handler]):
    user_id: UserId

    def __init__(self, user_id: UserId):
        self.user_id = user_id
