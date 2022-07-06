from graphimporter.entities.Datapoint import Datapoint
from graphimporter.mappers.DatapointDtoMapper import DatapointDtoMapper


class DatapointSqlMapper(DatapointDtoMapper):

    def entity_to_dto_string(self, entity: Datapoint) -> str:
        template = "stateName = '{stateName}', countyName = '{countyName}', ageGroup = '{ageGroup}', " \
                   "gender = '{gender}', recordingDate = '{recordingDate}', cases = {cases}, deaths = {deaths}, " \
                   "recovered = {recovered}"
        return template.format(stateName=entity.get_state(), countyName=entity.get_county(),
                               ageGroup=entity.get_age_group(), gender=entity.get_gender(),
                               recordingDate=entity.get_date(), cases=entity.get_cases(), deaths=entity.get_deaths(),
                               recovered=entity.get_recovered())

    def entity_to_dto_identifiers_string(self, entity: Datapoint) -> str:
        template = "stateName = '{stateName}' AND countyName = '{countyName}' AND ageGroup = '{ageGroup}' AND " \
                   "gender = '{gender}' AND recordingDate = '{recordingDate}'"
        return template.format(stateName=entity.get_state(), countyName=entity.get_county(),
                               ageGroup=entity.get_age_group(),
                               gender=entity.get_gender(), recordingDate=entity.get_date())

    def dto_to_entity(self, dto) -> Datapoint:
        return Datapoint(dto["stateName"], dto["countyName"], dto["ageGroup"], dto["gender"], dto["recordingDate"],
                         dto["cases"], dto["deaths"], dto["recovered"])

    def dtos_to_entities(self, dtos_list) -> [Datapoint]:
        entities = []
        for dto in dtos_list:
            entities.append(self.dto_to_entity(dto))
        return entities
