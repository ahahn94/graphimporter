from graphimporter.entities.Datapoint import Datapoint
from graphimporter.interfaces.DatabaseConnection import DatabaseConnectionInterface
from graphimporter.mappers.DatapointDtoMapper import DatapointDtoMapper
from graphimporter.repositories.DatabaseRepository import DatabaseRepository


class Neo4jRepository(DatabaseRepository):
    __database_connection: DatabaseConnectionInterface
    __datapoint_dto_mapper: DatapointDtoMapper

    def __init__(self, database_connection, datapoint_node_mapper: DatapointDtoMapper):
        super().__init__(database_connection, datapoint_node_mapper)
        self.__database_connection = database_connection
        self.__datapoint_dto_mapper = datapoint_node_mapper

    def initialize(self):
        if not self.__database_connection.is_initialized():
            self.__database_connection.connect()

    def is_initialized(self):
        return self.__database_connection.is_initialized()

    def insert_datapoint(self, datapoint: Datapoint):
        statement = self.__get_create_statement_for_datapoint(datapoint)
        self.__database_connection.run_query(statement)

    def delete_datapoint(self, datapoint: Datapoint):
        statement = self.__get_delete_statement_for_datapoint(datapoint)
        self.__database_connection.run_query(statement)

    def read_datapoint(self, datapoint: Datapoint):
        template = 'MATCH (d: {datapointCoordinates}) RETURN d LIMIT 1'
        datapoint_coordinates = self.__datapoint_dto_mapper.entity_to_dto_identifiers_string(datapoint)
        statement = template.format(datapointCoordinates=datapoint_coordinates)
        result = self.__database_connection.run_query(statement)
        return self.__datapoint_dto_mapper.dto_to_entity(result[0][0])

    def datapoint_exists(self, datapoint: Datapoint) -> bool:
        template = "OPTIONAL MATCH (d: {datapointDefinition}) RETURN d IS NOT NULL AS Exists"
        statement = template.format(datapointDefinition=self.__datapoint_dto_mapper.entity_to_dto_string(datapoint))
        result_2d_array = self.__database_connection.run_query(statement)
        exists = result_2d_array[0][0]
        return exists

    def add_neighbour_county_relationship(self, base_county: str, neighbour_county: str):
        template = f"MATCH (base: Datapoint) MATCH(neighbour: Datapoint) " \
                   f"WHERE base.countyName =~ '{base_county}' AND neighbour.countyName =~ '{neighbour_county}' AND " \
                   f"base.countyName <> neighbour.countyName AND " \
                   f"neighbour.ageGroup = base.ageGroup AND " \
                   f"neighbour.date = base.date AND neighbour.gender = base.gender CREATE (base)-[" \
                   f"r:NEIGHBOUR_COUNTY]->(neighbour) RETURN r "
        statement = template.format(base_county=base_county, neighbour_county=neighbour_county)
        self.__database_connection.run_query(statement)

    def get_neighbours(self, datapoint: Datapoint):
        template = "MATCH (base: {baseCounty})-[r:NEIGHBOUR_COUNTY]->(neighbour) RETURN neighbour"
        base_county = self.__datapoint_dto_mapper.entity_to_dto_identifiers_string(datapoint)
        statement = template.format(baseCounty=base_county)
        result_2d_array = self.__database_connection.run_query(statement)
        return self.__datapoint_dto_mapper.dtos_to_entities(result_2d_array[0])

    def add_gender_relationships(self):
        statement = "MATCH (n: Datapoint)" \
                    "WITH collect(DISTINCT n.date) AS dates" \
                    "UNWIND dates AS date" \
                    "MATCH (a: Datapoint{date: date}) MATCH (b: Datapoint{date: date})" \
                    "WHERE a.date = b.date AND a.gender <> b.gender AND a.ageGroup = b.ageGroup " \
                    "AND a.countyName = b.countyName" \
                    "CREATE (a)-[r: OTHER_GENDER]->(b)" \
                    "WITH count(r) AS createdCount" \
                    "RETURN createdCount"
        self.__database_connection.run_query(statement)

    def add_younger_relationship(self, younger: str, older: str):
        template = "MATCH (a: Datapoint) Match (b: Datapoint) " \
                   "WHERE a.ageGroup = \"{younger}\" AND b.ageGroup = \"{older}\" " \
                   "AND a.gender = b.gender " \
                   "AND a.date = b.date " \
                   "AND a.countyName = b.countyName " \
                   "CREATE (a)-[r: IS_ONE_YOUNGER_THAN]->(b) RETURN r"
        statement = template.format(younger=younger, older=older)
        self.__database_connection.run_query(statement)

    def add_older_relationship(self, older: str, younger: str):
        template = "MATCH (a: Datapoint) Match (b: Datapoint) " \
                   "WHERE a.ageGroup = \"{older}\" AND b.ageGroup = \"{younger}\" " \
                   "AND a.gender = b.gender " \
                   "AND a.date = b.date " \
                   "AND a.countyName = b.countyName " \
                   "CREATE (a)-[r: IS_ONE_OLDER_THAN]->(b) RETURN r"
        statement = template.format(younger=younger, older=older)
        self.__database_connection.run_query(statement)

    def add_previous_day_relationship(self, previous_day: str, current_day: str):
        template = "MATCH (a: Datapoint) Match (b: Datapoint) " \
                   "WHERE a.date = \"{previousDay}\" AND b.date = \"{currentDay}\" " \
                   "AND a.ageGroup = b.ageGroup " \
                   "AND a.gender = b.gender " \
                   "AND a.countyName = b.countyName " \
                   "CREATE (a)-[r: IS_PREVIOUS_DAY_TO]->(b) RETURN r"
        statement = template.format(previousDay=previous_day, currentDay=current_day)
        self.__database_connection.run_query(statement)

    def add_next_day_relationship(self, next_day: str, current_day: str):
        template = "MATCH (a: Datapoint) Match (b: Datapoint) " \
                   "WHERE a.date = \"{nextDay}\" AND b.date = \"{currentDay}\" " \
                   "AND a.ageGroup = b.ageGroup " \
                   "AND a.gender = b.gender " \
                   "AND a.countyName = b.countyName " \
                   "CREATE (a)-[r: IS_NEXT_DAY_TO]->(b) RETURN r"
        statement = template.format(nextDay=next_day, currentDay=current_day)
        self.__database_connection.run_query(statement)

    def __get_create_statement_for_datapoint(self, datapoint: Datapoint):
        template = "CREATE (d: {datapointDefinition});"
        return template.format(datapointDefinition=self.__datapoint_dto_mapper.entity_to_dto_string(datapoint))

    def __get_delete_statement_for_datapoint(self, datapoint: Datapoint):
        template = "MATCH (d: {datapointCoordinates}) DETACH DELETE d;"
        datapoint_coordinates = self.__datapoint_dto_mapper.entity_to_dto_identifiers_string(datapoint)
        return template.format(datapointCoordinates=datapoint_coordinates)
