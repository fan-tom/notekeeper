# REVIEW M1ha:
#  1. Почему exception находится в commands_deserializers? Это же не сериализатор ни разу.
#  2. Стандартный Exception делает именно это, записывая первый атрибут в self.details.
#    Зачем собственная реализация?
#    Можно было тупо сделать, если нужен свой exception на базе Exception:
#    class DeserializeException(Exception):
#        pass

class DeserializeException(Exception):
    """Exception thrown when cannot deserialize exception"""

    description: str

    def __init__(self, description: str):
        self.description = description
