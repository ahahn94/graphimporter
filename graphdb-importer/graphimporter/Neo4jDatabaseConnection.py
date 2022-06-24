from typing import Union, Any

from neo4j import GraphDatabase, Neo4jDriver
from neo4j.exceptions import AuthError, ServiceUnavailable

from graphimporter.exceptions.WrongDatabaseCredentialsException import WrongDatabaseCredentialsException
from graphimporter.exceptions.WrongDatabaseServerUriException import WrongDatabaseServerUriException
from graphimporter.interfaces.DatabaseConnection import DatabaseConnectionInterface


class Neo4jDatabaseConnection(DatabaseConnectionInterface):

    __driver: Union[Neo4jDriver, Any] = None

    def __init__(self, server_uri: str, username: str, password: str):
        self.__server_uri = server_uri
        self.__username = username
        self.__password = password

    def connect(self):
        driver = GraphDatabase.driver(self.__server_uri, auth=(self.__username, self.__password))
        try:
            self.__test_connection(driver)
            self.__driver = driver
        except AuthError:
            raise WrongDatabaseCredentialsException
        except (ConnectionError, ServiceUnavailable):
            raise WrongDatabaseServerUriException

    @staticmethod
    def __test_connection(driver):
        with driver.session() as session:
            session.run("MATCH () RETURN 1 LIMIT 1")

    def run_query(self, query):
        with self.__driver.session() as session:
            result = session.run(query)
            return result.values()

    def is_initialized(self) -> bool:
        return self.__driver is not None
