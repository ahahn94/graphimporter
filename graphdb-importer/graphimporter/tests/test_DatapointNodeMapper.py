import unittest

from graphimporter.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.entities.Datapoint import Datapoint


class DatapointNodeMapperTest(unittest.TestCase):
    __test_datapoint = Datapoint("Test-Land", "Test-Kreis A", "00-04", "X", "2022-06-21", 0, 0, 0)
    __test_node = {
        "stateName": "Test-Land",
        "countyName": "Test-Kreis A",
        "ageGroup": "00-04",
        "gender": "X",
        "date": "2022-06-21",
        "casesCount": 0,
        "deathsCount": 0,
        "recoveredCount": 0
    }

    @classmethod
    def setUpClass(cls):
        cls.__datapoint_node_mapper = DatapointNodeMapper()

    def test_datapoint_to_node_string(self):
        expected = 'Datapoint {stateName: "Test-Land", countyName: "Test-Kreis A", ageGroup: "00-04", gender: "X", ' \
                   'date: "2022-06-21", casesCount: 0, deathsCount: 0, recoveredCount: 0}'
        node_string = self.__datapoint_node_mapper.entity_to_node_string(self.__test_datapoint)
        self.assertEqual(node_string, expected)

    def test_datapoint_to_node_coordinates_string(self):
        expected = 'Datapoint {stateName: "Test-Land", countyName: "Test-Kreis A", ageGroup: "00-04", gender: "X", ' \
                   'date: "2022-06-21"}'
        node_string = self.__datapoint_node_mapper.entity_to_node_coordinates_string(self.__test_datapoint)
        self.assertEqual(node_string, expected)

    def test_node_to_entity(self):
        entity = self.__datapoint_node_mapper.node_to_entity(self.__test_node)
        self.assertEqual(entity, self.__test_datapoint)

    def test_nodes_to_entities(self):
        entities = self.__datapoint_node_mapper.nodes_to_entities([self.__test_node])
        self.assertIn(self.__test_datapoint, entities)


if __name__ == '__main__':
    unittest.main()
