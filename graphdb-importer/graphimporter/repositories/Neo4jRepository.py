import neo4j.graph

from graphimporter.Neo4jDatabaseConnection import Neo4jDatabaseConnection
from graphimporter.entities.Datapoint import Datapoint


class Neo4jRepository:
    __neo4j_database_connection: Neo4jDatabaseConnection

    def __init__(self, neo4j_database_connection):
        self.__neo4j_database_connection = neo4j_database_connection

    def initialize(self):
        if not self.__neo4j_database_connection.is_initialized():
            self.__neo4j_database_connection.connect()

    def is_initialized(self):
        return self.__neo4j_database_connection.is_initialized()

    def insert_datapoint(self, datapoint):
        statement = self.__get_create_statement_for_datapoint(datapoint)
        self.__neo4j_database_connection.run_query(statement)

    def delete_datapoint(self, datapoint):
        statement = self.__get_delete_statement_for_datapoint(datapoint)
        self.__neo4j_database_connection.run_query(statement)

    def read_datapoint(self, date, county, age_group, gender):
        statement = f'MATCH (r: Record {{date: "{date}", countyName: "{county}", ageGroup: "{age_group}", ' \
                    f'gender: "{gender}"}}) RETURN r LIMIT 1'
        result = self.__neo4j_database_connection.run_query(statement)
        return self.__node_to_dataset(result[0][0])

    @staticmethod
    def __get_create_statement_for_datapoint(datapoint):
        return f"CREATE (r:Record {{" \
               f"stateName: \"{datapoint.get_state()}\", " \
               f"countyName: \"{datapoint.get_county()}\", " \
               f"ageGroup: \"{datapoint.get_age_group()}\", " \
               f"gender: \"{datapoint.get_gender()}\", " \
               f"date: \"{datapoint.get_date()}\", " \
               f"casesCount: {datapoint.get_cases()}, " \
               f"deathsCount: {datapoint.get_deaths()}, " \
               f"recoveredCount: {datapoint.get_recovered()}" \
               f"}});"

    @staticmethod
    def __get_delete_statement_for_datapoint(datapoint):
        return f"MATCH (r:Record {{stateName: \"{datapoint.get_state()}\", countyName: \"{datapoint.get_county()}\", " \
               f"ageGroup: \"{datapoint.get_age_group()}\", gender: \"{datapoint.get_gender()}\", " \
               f"date: \"{datapoint.get_date()}\"}}) DELETE r;"

    @staticmethod
    def __node_to_dataset(node: neo4j.graph.Node):
        return Datapoint(node["stateName"], node["countyName"], node["ageGroup"], node["gender"], node["date"],
                         node["casesCount"], node["deathsCount"], node["recoveredCount"])
