from abc import ABC

from graphimporter.entities.Datapoint import Datapoint


class DatapointDtoMapper(ABC):

    def entity_to_dto_string(self, entity: Datapoint) -> str:
        pass

    def entity_to_dto_identifiers_string(self, entity: Datapoint) -> str:
        pass

    def dto_to_entity(self, dto) -> Datapoint:
        pass

    def dtos_to_entities(self, dtos_list) -> [Datapoint]:
        pass
