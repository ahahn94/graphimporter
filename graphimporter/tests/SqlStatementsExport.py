import unittest

from graphimporter.GraphImporter import GraphImporter
from graphimporter.LoggingDummyDatabaseConnection import LoggingDummyDatabaseConnection
from graphimporter.mappers.DatapointSqlMapper import DatapointSqlMapper
from graphimporter.repositories.SqlRepository import SqlRepository


class SqlStatementsExport(unittest.TestCase):
    __dummy_database_connection = LoggingDummyDatabaseConnection("testfiles/exported_statements.sql", "", "")
    __datapoint_node_mapper = DatapointSqlMapper()
    __path_to_shape_file = "testfiles/de_county.shp"
    __path_to_dataset_file = "testfiles/january_2022_first_day.csv"

    def test_something(self):
        self.__dummy_database_connection.connect()
        database_repository = SqlRepository(self.__dummy_database_connection, self.__datapoint_node_mapper)
        graph_importer = GraphImporter(database_repository, self.__path_to_dataset_file, self.__path_to_shape_file)
        graph_importer.import_datasets_and_relationships()


if __name__ == '__main__':
    unittest.main()
