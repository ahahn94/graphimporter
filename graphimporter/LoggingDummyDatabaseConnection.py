from typing import TextIO

from graphimporter.interfaces.DatabaseConnection import DatabaseConnectionInterface


class LoggingDummyDatabaseConnection(DatabaseConnectionInterface):

    __log_file: TextIO = None
    __query_log_filepath: str

    def __init__(self, server_uri: str, username: str, password: str):
        super().__init__(server_uri, username, password)
        self.__query_log_filepath = server_uri

    def connect(self):
        self.__log_file = open(self.__query_log_filepath, "w")
        print(self.__log_file)
        pass

    def run_query(self, query):
        if "OPTIONAL MATCH" in query:
            # Checking if a datapoint exists. Return False in 2d list.
            return [[False]]
        self.__log_file.write(query + "\n")

    def is_initialized(self) -> bool:
        return self.__log_file is not None

    def __del__(self):
        self.__log_file.close()
