from graphimporter.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.entities.Datapoint import Datapoint
from graphimporter.interfaces.DatabaseConnection import DatabaseConnectionInterface


class Neo4jRepository:
    __neo4j_database_connection: DatabaseConnectionInterface
    __datapoint_node_mapper: DatapointNodeMapper

    def __init__(self, neo4j_database_connection, datapoint_node_mapper: DatapointNodeMapper):
        self.__neo4j_database_connection = neo4j_database_connection
        self.__datapoint_node_mapper = datapoint_node_mapper

    def initialize(self):
        if not self.__neo4j_database_connection.is_initialized():
            self.__neo4j_database_connection.connect()

    def is_initialized(self):
        return self.__neo4j_database_connection.is_initialized()

    def insert_datapoint(self, datapoint: Datapoint):
        statement = self.__get_create_statement_for_datapoint(datapoint)
        self.__neo4j_database_connection.run_query(statement)

    def delete_datapoint(self, datapoint: Datapoint):
        statement = self.__get_delete_statement_for_datapoint(datapoint)
        self.__neo4j_database_connection.run_query(statement)

    def read_datapoint(self, datapoint: Datapoint):
        template = 'MATCH (d: {datapointCoordinates}) RETURN d LIMIT 1'
        datapoint_coordinates = self.__datapoint_node_mapper.entity_to_node_coordinates_string(datapoint)
        statement = template.format(datapointCoordinates=datapoint_coordinates)
        result = self.__neo4j_database_connection.run_query(statement)
        return self.__datapoint_node_mapper.node_to_entity(result[0][0])

    def datapoint_exists(self, datapoint: Datapoint) -> bool:
        template = "OPTIONAL MATCH (d: {datapointDefinition}) RETURN d IS NOT NULL AS Exists"
        statement = template.format(datapointDefinition=self.__datapoint_node_mapper.entity_to_node_string(datapoint))
        result_2d_array = self.__neo4j_database_connection.run_query(statement)
        exists = result_2d_array[0][0]
        return exists

    def add_neighbour_county_relationship(self, base_county: str, neighbour_county: str):
        template = f"MATCH (base: Datapoint) MATCH(neighbour: Datapoint) " \
                   f"WHERE base.countyName = '{base_county}' AND neighbour.countyName = '{neighbour_county}' AND " \
                   f"base.countyName <> neighbour.countyName AND " \
                   f"neighbour.ageGroup = base.ageGroup AND " \
                   f"neighbour.date = base.date AND neighbour.gender = base.gender CREATE (base)-[" \
                   f"r:NEIGHBOUR_COUNTY]->(neighbour) RETURN r "
        statement = template.format(base_county=base_county, neighbour_county=neighbour_county)
        self.__neo4j_database_connection.run_query(statement)

    def get_neighbours(self, datapoint: Datapoint):
        template = "MATCH (base: {baseCounty})-[r:NEIGHBOUR_COUNTY]->(neighbour) RETURN neighbour"
        base_county = self.__datapoint_node_mapper.entity_to_node_coordinates_string(datapoint)
        statement = template.format(baseCounty=base_county)
        result_2d_array = self.__neo4j_database_connection.run_query(statement)
        return self.__datapoint_node_mapper.nodes_to_entities(result_2d_array[0])

    def __get_create_statement_for_datapoint(self, datapoint: Datapoint):
        template = "CREATE (d: {datapointDefinition});"
        return template.format(datapointDefinition=self.__datapoint_node_mapper.entity_to_node_string(datapoint))

    def __get_delete_statement_for_datapoint(self, datapoint: Datapoint):
        template = "MATCH (d: {datapointCoordinates}) DETACH DELETE d;"
        datapoint_coordinates = self.__datapoint_node_mapper.entity_to_node_coordinates_string(datapoint)
        return template.format(datapointCoordinates=datapoint_coordinates)
