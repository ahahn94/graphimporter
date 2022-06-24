import unittest
from typing import TextIO

from graphimporter.GraphImporter import GraphImporter
from graphimporter.interfaces.DatabaseConnection import DatabaseConnectionInterface


class LoggingDummyDatabaseConnection(DatabaseConnectionInterface):

    __log_file: TextIO = None
    __query_log_filepath = "testfiles/exported_statements.cypher"

    def __init__(self, server_uri: str, username: str, password: str):
        super().__init__(server_uri, username, password)

    def connect(self):
        self.__log_file = open(self.__query_log_filepath, "w")
        pass

    def run_query(self, query):
        if "OPTIONAL MATCH" in query:
            # Checking if a datapoint exists. Return False in 2d list.
            return [[False]]
        self.__log_file.write(query + "\n")

    def is_initialized(self) -> bool:
        return True

    def __del__(self):
        self.__log_file.close()


class CypherStatementsExport(unittest.TestCase):
    __dummy_database_connection = LoggingDummyDatabaseConnection("", "", "")
    __path_to_shape_file = "testfiles/de_county.shp"
    __path_to_dataset_file = "testfiles/covid_de_testing.csv"

    def test_something(self):
        self.__dummy_database_connection.connect()
        graph_importer = GraphImporter(self.__dummy_database_connection, self.__path_to_dataset_file,
                                      self.__path_to_shape_file)
        graph_importer.import_datasets()
        graph_importer.create_relations()


if __name__ == '__main__':
    unittest.main()
