from collections import Counter
from typing import List

from graphimporter.UnmergeableCountiesException import UnmergeableCountiesException
from graphimporter.entities.County import County
from graphimporter.entities.CountyType import CountyType


class ShapeCounty(County):
    __neighbours: List[str]

    def __init__(self, name: str, county_type: CountyType, canonic_name: str, neighbours):
        super().__init__(name, county_type, canonic_name)
        self.__neighbours = self.__deduplicate_neighbours(neighbours)

    def get_neighbours(self):
        return self.__neighbours

    def __str__(self) -> str:
        return "'name': {}, 'canonic_name': {}, 'neighbours': {}".format(self._name, self._canonic_name,
                                                                         self.__neighbours)

    def merge(self, other: 'ShapeCounty'):
        if self.same_county(other):
            neighbours = self.__merge_neighbours(other)
            return ShapeCounty(self._name, self._county_type, self._canonic_name, neighbours)
        else:
            raise UnmergeableCountiesException

    def __merge_neighbours(self, other):
        neighbours = self.__neighbours + other.__neighbours
        deduplicated_neighbours = self.__deduplicate_neighbours(neighbours)
        return deduplicated_neighbours

    def __deduplicate_neighbours(self, neighbours):
        unique_neighbours = set(neighbours)
        if self._canonic_name in unique_neighbours:
            unique_neighbours.remove(self._canonic_name)
        return list(unique_neighbours)

    def equals(self, other: 'ShapeCounty'):
        county_matches = self.same_county(other)
        neighbours_match = self.__same_neighbours(other)
        return county_matches and neighbours_match

    def __same_neighbours(self, other):
        return Counter(self.__neighbours) == Counter(other.get_neighbours())
