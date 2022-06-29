import unittest

from graphimporter.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.GraphImporter import GraphImporter
from graphimporter.LoggingDummyDatabaseConnection import LoggingDummyDatabaseConnection
from graphimporter.repositories.Neo4jRepository import Neo4jRepository


class CypherStatementsExport(unittest.TestCase):
    __dummy_database_connection = LoggingDummyDatabaseConnection("testfiles/exported_statements.cypher", "", "")
    __datapoint_node_mapper = DatapointNodeMapper()
    __path_to_shape_file = "testfiles/de_county.shp"
    __path_to_dataset_file = "testfiles/covid_de_testing.csv"

    def test_something(self):
        self.__dummy_database_connection.connect()
        database_repository = Neo4jRepository(self.__dummy_database_connection, self.__datapoint_node_mapper)
        graph_importer = GraphImporter(database_repository, self.__path_to_dataset_file,
                                      self.__path_to_shape_file)
        graph_importer.import_datasets_and_relationships()


if __name__ == '__main__':
    unittest.main()
