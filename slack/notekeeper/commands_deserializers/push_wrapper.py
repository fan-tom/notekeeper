from core.commands import Push
from core.entities import Note
from .deserialize_exception import DeserializeException
from .identified_wrapper import IdentifiedCommandWrapper


class PushWrapper(IdentifiedCommandWrapper[Push, Note]):
    """Deserialize arguments for Push command"""

    command_class = Push

    def deserialize(self, input: str) -> Push:
        if input is None:
            raise DeserializeException(f"note text is not specified")
        return Push(self.user_id, input)

    def serialize(self, output: Note) -> str:
        return f"Note was saved with id {output.id}"
