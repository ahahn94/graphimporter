from abc import ABC

from graphimporter.mappers.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.entities.Datapoint import Datapoint


class DatabaseRepository(ABC):

    def __init__(self, database_connection, datapoint_node_mapper: DatapointNodeMapper):
        pass

    def initialize(self):
        pass

    def is_initialized(self):
        pass

    def insert_datapoint(self, datapoint: Datapoint):
        pass

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
