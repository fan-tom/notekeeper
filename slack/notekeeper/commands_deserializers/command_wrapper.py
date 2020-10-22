from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, ClassVar, Type

from core.interfaces import Command

C = TypeVar('C', bound=Command)  # command type
O = TypeVar('O')  # command output type


class CommandWrapper(ABC, Generic[C, O]):
    """Wrapper to deserialize command from string and serialize result"""

    command_class: ClassVar[Type[C]]  # corresponding command class


    @abstractmethod
    def deserialize(self, input: str) -> C:
        """Deserialize command of type C from string"""
        pass

    @abstractmethod
    def serialize(self, output: Optional[O]) -> Optional[str]:
        """Serialize command result to string, if any"""
        pass