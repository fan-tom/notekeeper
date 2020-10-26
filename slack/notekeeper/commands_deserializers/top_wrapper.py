from typing import List

from core.commands import Top
from core.entities import Note
from .deserialize_exception import DeserializeException
from .identified_wrapper import IdentifiedCommandWrapper


# REVIEW M1ha:
#  Та же фигня, что и с PushWrapper: сериализуем одно, десериализуем другое.

class TopWrapper(IdentifiedCommandWrapper[Top, List[Note]]):
    """Deserialize arguments for Top command"""

    command_class = Top

    def deserialize(self, input: str) -> Top:
        if input is None:
            n = None
        else:
            try:
                n = int(input)
            except ValueError:
                raise DeserializeException(f"required numeric argument, got {input}")
        return Top(self.user_id, n)

    def serialize(self, output: List[Note]) -> str:
        notes_number = len(output)
        if notes_number > 0:
            content = '\n\n'.join((f"Id: {note.id}\nCreated at: {note.created_at}\nText: {note.text}" for note in output))
            return f"Last {'note' if notes_number == 1 else f'{notes_number} notes'}:\n\n{content}"
        else:
            return "No notes"
