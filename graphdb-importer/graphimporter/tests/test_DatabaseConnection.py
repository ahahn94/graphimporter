import unittest

import neo4j.exceptions

from graphimporter.Neo4jDatabaseConnection import Neo4jDatabaseConnection
from graphimporter.exceptions.WrongDatabaseCredentialsException import WrongDatabaseCredentialsException
from graphimporter.exceptions.WrongDatabaseServerUriException import WrongDatabaseServerUriException


class Neo4jDatabaseConnectionTest(unittest.TestCase):
    __server_uri: str = None
    __username: str = None
    __password: str = None

    @classmethod
    def setUpClass(cls):
        cls.__server_uri = "bolt://127.0.0.1:7687"
        cls.__username = "neo4j"
        cls.__password = "graphdb"
        cls.__neo4j_database_connection = Neo4jDatabaseConnection(cls.__server_uri, cls.__username, cls.__password)

    def test_connecting(self):
        self.__neo4j_database_connection.connect()
        self.assertEqual(self.__neo4j_database_connection.is_initialized(), True)

    def test_connecting_faulty_credentials_raises_exception(self):
        faulty_password = "wrongpassword"
        neo4j_database_connection = Neo4jDatabaseConnection(self.__server_uri, self.__username, faulty_password)
        with (self.assertRaises(WrongDatabaseCredentialsException)):
            neo4j_database_connection.connect()

    def test_connecting_faulty_server_uri_raises_exception(self):
        faulty_server_uri = "bolt://127.0.0.1:7777"
        neo4j_database_connection = Neo4jDatabaseConnection(faulty_server_uri, self.__username, self.__password)
        with (self.assertRaises(WrongDatabaseServerUriException)):
            neo4j_database_connection.connect()

    def test_run_query(self):
        statement = "OPTIONAL MATCH (n) RETURN n IS NOT NULL AS Exists"
        result = self.__neo4j_database_connection.run_query(statement)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0][0], bool)

    def test_run_query_faulty_statement_raises_exceptions(self):
        statement = "MATCH (n) RETURN n LIMIT "
        with (self.assertRaises(neo4j.exceptions.Neo4jError)):
            self.__neo4j_database_connection.run_query(statement)


if __name__ == '__main__':
    unittest.main()
