from graphimporter.entities.Datapoint import Datapoint
from graphimporter.interfaces import DatabaseConnection
from graphimporter.mappers.DatapointDtoMapper import DatapointDtoMapper
from graphimporter.repositories.DatabaseRepository import DatabaseRepository


class SqlRepository(DatabaseRepository):
    __database_connection: DatabaseConnection
    __datapoint_dto_mapper: DatapointDtoMapper

    def __init__(self, database_connection, datapoint_dto_mapper: DatapointDtoMapper):
        super().__init__(database_connection, datapoint_dto_mapper)
        self.__database_connection = database_connection
        self.__datapoint_dto_mapper = datapoint_dto_mapper

    def initialize(self):
        if not self.__database_connection.is_initialized():
            self.__database_connection.connect()
        self.__setup_tables()

    def is_initialized(self):
        return self.__database_connection.is_initialized()

    def insert_datapoint(self, datapoint: Datapoint):
        template = 'INSERT INTO datapoints SET {dto};'
        statement = template.format(dto=self.__datapoint_dto_mapper.entity_to_dto_string(datapoint))
        self.__database_connection.run_query(statement)

    def delete_datapoint(self, datapoint: Datapoint):
        pass

    def read_datapoint(self, datapoint: Datapoint):
        pass

    def datapoint_exists(self, datapoint: Datapoint) -> bool:
        pass

    def add_neighbour_county_relationship(self, base_county: str, neighbour_county: str):
        pass

    def get_neighbours(self, datapoint: Datapoint):
        pass

    def add_gender_relationships(self):
        pass

    def add_younger_relationship(self, younger: str, older: str):
        pass

    def add_older_relationship(self, older: str, younger: str):
        pass

    def add_previous_day_relationship(self, previous_day: str, current_day: str):
        pass

    def add_next_day_relationship(self, next_day: str, current_day: str):
        pass

    def __setup_tables(self):
        self.__setup_records_table()

    def __setup_records_table(self):
        statement = "CREATE TABLE IF NOT EXISTS datapoints (stateName TINYTEXT, countyName TINYTEXT, ageGroup TINYTEXT, gender TINYTEXT, recordingDate TINYTEXT, cases INT DEFAULT 0, deaths INT DEFAULT 0, recovered INT DEFAULT 0);"
        self.__database_connection.run_query(statement)
        print(statement)
