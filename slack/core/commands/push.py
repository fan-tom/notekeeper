from abc import abstractmethod, ABC

from core.entities.note import UserId, Note
from core.interfaces import IdentifiedCommand

# REVIEW M1ha:
#   1. Зачем столько описаний интерфейсов, которые по сути ничего не дают?
#   2. Зачем выделять отдельный handler? Опять же лишняя сущность с непонятной целью, достаточно метода handle.
#   3. Почему интерфейсы лежат аж в отдельном package от реализации? С какой целью?
#     Вероятность реализации такой же push команды стремится к 0 => Переиспользовать интерфейс нельзя.
#     Я бы вообще честно говоря, не плодил кучу незначимых интерфейсов.
#     Только если они логически объединяют или задают структуру какого-то компонента.
#     Например, абстрактной команды. Или бота.


class PushHandler(ABC):
    """
    Push command executor interface
    """
    @abstractmethod
    def handle_push(self, command: 'Push') -> Note:
        pass


class Push(IdentifiedCommand[PushHandler]):
    """Add note to list"""

    text: str  # Note text

    # REVIEW M1ha: Зачем определеять свой тип для UserID? Больше ссылок богу ссылок?
    #   Будь тут прямо написано, что это UUID, все было бы очевидно
    def __init__(self, user_id: UserId, text: str):
        super().__init__(user_id)
        self.text = text

    def handle(self, handler: PushHandler) -> Note:
        return handler.handle_push(self)
