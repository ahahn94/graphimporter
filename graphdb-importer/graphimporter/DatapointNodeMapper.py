from graphimporter.entities.Datapoint import Datapoint


class DatapointNodeMapper:

    def entity_to_node_string(self, entity: Datapoint):
        template = "Datapoint {{{coordinates}, " \
                   "{values}}}"
        return template.format(coordinates=self.__get_prepared_coordinates_string(entity),
                               values=self.__get_prepared_values_string(entity))

    def entity_to_node_coordinates_string(self, entity: Datapoint):
        template = "Datapoint {{{coordinates}}}"
        return template.format(coordinates=self.__get_prepared_coordinates_string(entity))

    def node_to_entity(self, node):
        return Datapoint(node["stateName"], node["countyName"], node["ageGroup"], node["gender"], node["date"],
                         node["casesCount"], node["deathsCount"], node["recoveredCount"])

    def nodes_to_entities(self, nodes_list):
        entities = []
        for node in nodes_list:
            entities.append(self.node_to_entity(node))
        return entities

    def __get_prepared_coordinates_string(self, entity: Datapoint):
        template = "stateName: \"{state}\", countyName: \"{county}\", ageGroup: \"{age_group}\", " \
                   "gender: \"{gender}\", date: \"{date}\""
        return template.format(state=entity.get_state(), county=entity.get_county(), age_group=entity.get_age_group(),
                               gender=entity.get_gender(), date=entity.get_date())

    def __get_prepared_values_string(self, entity: Datapoint):
        template = "casesCount: {cases}, deathsCount: {deaths}, recoveredCount: {recovered}"
        return template.format(cases=entity.get_cases(), deaths=entity.get_deaths(), recovered=entity.get_recovered())
