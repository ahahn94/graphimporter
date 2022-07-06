from abc import ABC


class DatabaseConnectionInterface(ABC):

    def __init__(self, server_uri: str, username: str, password: str):
        pass

    def connect(self):
        pass

    def run_query(self, query):
        pass

    def is_initialized(self) -> bool:
        pass
