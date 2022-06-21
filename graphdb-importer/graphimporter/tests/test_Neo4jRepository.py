import unittest

from graphimporter.Neo4jDatabaseConnection import Neo4jDatabaseConnection
from graphimporter.entities.Datapoint import Datapoint
from graphimporter.repositories.Neo4jRepository import Neo4jRepository


class Neo4jRepositoryTest(unittest.TestCase):
    __server_uri: str = "bolt://127.0.0.1:7687"
    __username: str = "neo4j"
    __password: str = "graphdb"
    __neo4j_repository: Neo4jRepository = None

    __test_datapoint_1 = Datapoint("Test-Land", "Test-Kreis A", "00-04", "X", "2022-06-21", 0, 0, 0)

    @classmethod
    def setUpClass(cls):
        cls.__neo4j_repository = Neo4jRepository(
            Neo4jDatabaseConnection(cls.__server_uri, cls.__username, cls.__password))
        cls.__neo4j_repository.initialize()

    def test_initialize(self):
        neo4j_repository = Neo4jRepository(Neo4jDatabaseConnection(self.__server_uri, self.__username, self.__password))
        neo4j_repository.initialize()
        self.assertEqual(neo4j_repository.is_initialized(), True)

    def test_insert_and_read_datapoint(self):
        self.__neo4j_repository.insert_datapoint(self.__test_datapoint_1)
        datapoint = self.__neo4j_repository.read_datapoint(
            self.__test_datapoint_1.get_date(),
            self.__test_datapoint_1.get_county(),
            self.__test_datapoint_1.get_age_group(),
            self.__test_datapoint_1.get_gender())
        self.assertEqual(datapoint, self.__test_datapoint_1)

    @classmethod
    def tearDownClass(cls):
        cls.__neo4j_repository.delete_datapoint(cls.__test_datapoint_1)


if __name__ == '__main__':
    unittest.main()
