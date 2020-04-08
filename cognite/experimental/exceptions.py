class ModelFailedException(Exception):
    def __init__(self, type, id, error_message):
        self.type = type
        self.id = id
        self.error_message = error_message

    def __str__(self):
        return f"{self.type} {self.id} failed with error '{self.error_message}'"
