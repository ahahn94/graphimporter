import unittest

from graphimporter.mappers.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.Neo4jDatabaseConnection import Neo4jDatabaseConnection
from graphimporter.entities.Datapoint import Datapoint
from graphimporter.repositories.Neo4jRepository import Neo4jRepository


class Neo4jRepositoryTest(unittest.TestCase):
    __server_uri: str = "bolt://127.0.0.1:7687"
    __username: str = "neo4j"
    __password: str = "graphdb"
    __neo4j_repository: Neo4jRepository = None
    __datapoint_node_mapper: DatapointNodeMapper = None

    __datapoint_insert_delete = Datapoint("Test-Land", "Test-Kreis A", "00-04", "X", "2022-06-21", 0, 0, 0)
    __datapoint_setup_exists_read_teardown = Datapoint("Test-Land", "Test-Kreis B", "00-04", "X", "2022-06-21", 0, 0, 0)
    __datapoint_setup_neighbour_relationship_teardown = Datapoint("Test-Land", "Test-Kreis C", "00-04", "X",
                                                                  "2022-06-21", 0, 0, 0)

    @classmethod
    def setUpClass(cls):
        neo4j_database_connection = Neo4jDatabaseConnection(cls.__server_uri, cls.__username, cls.__password)
        cls.__datapoint_node_mapper = DatapointNodeMapper()
        cls.__neo4j_repository = Neo4jRepository(neo4j_database_connection, cls.__datapoint_node_mapper)
        cls.__neo4j_repository.initialize()
        cls.__neo4j_repository.insert_datapoint(cls.__datapoint_setup_exists_read_teardown)
        cls.__neo4j_repository.insert_datapoint(cls.__datapoint_setup_neighbour_relationship_teardown)

    def test_initialize(self):
        neo4j_database_connection = Neo4jDatabaseConnection(self.__server_uri, self.__username, self.__password)
        neo4j_repository = Neo4jRepository(neo4j_database_connection, self.__datapoint_node_mapper)
        neo4j_repository.initialize()
        self.assertEqual(neo4j_repository.is_initialized(), True)

    def test_insert_delete_datapoint(self):
        self.__test_insert()
        self.__test_delete()

    def __test_insert(self):
        self.__neo4j_repository.insert_datapoint(self.__datapoint_insert_delete)
        self.assertEqual(self.__neo4j_repository.datapoint_exists(self.__datapoint_insert_delete), True)

    def __test_delete(self):
        self.__neo4j_repository.delete_datapoint(self.__datapoint_insert_delete)
        self.assertEqual(self.__neo4j_repository.datapoint_exists(self.__datapoint_insert_delete), False)

    def test_datapoint_exists(self):
        self.assertEqual(self.__neo4j_repository.datapoint_exists(self.__datapoint_setup_exists_read_teardown), True)

    def test_read_datapoint(self):
        datapoint_from_database = self.__neo4j_repository.read_datapoint(self.__datapoint_setup_exists_read_teardown)
        self.assertEqual(datapoint_from_database, self.__datapoint_setup_exists_read_teardown)

    def test_add_get_neighbour_county_relationship(self):
        self.__test_add_neighbour_relationship()
        neighbours = self.__neo4j_repository.get_neighbours(self.__datapoint_setup_exists_read_teardown)
        self.assertIsInstance(neighbours, list)
        self.assertIn(self.__datapoint_setup_neighbour_relationship_teardown, neighbours)

    def __test_add_neighbour_relationship(self):
        base_county = self.__datapoint_setup_exists_read_teardown.get_county()
        neighbour_county = self.__datapoint_setup_neighbour_relationship_teardown.get_county()
        self.__neo4j_repository.add_neighbour_county_relationship(base_county, neighbour_county)

    @classmethod
    def tearDownClass(cls):
        cls.__neo4j_repository.delete_datapoint(cls.__datapoint_setup_exists_read_teardown)
        cls.__neo4j_repository.delete_datapoint(cls.__datapoint_setup_neighbour_relationship_teardown)


if __name__ == '__main__':
    unittest.main()
