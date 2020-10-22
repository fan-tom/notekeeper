class DeserializeException(Exception):
    """Exception thrown when cannot deserialize exception"""

    description: str

    def __init__(self, description: str):
        self.description = description
