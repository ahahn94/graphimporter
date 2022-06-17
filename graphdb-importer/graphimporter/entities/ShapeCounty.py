from typing import List

from graphimporter.entities.County import County
from graphimporter.entities.CountyType import CountyType


class ShapeCounty(County):

    __neighbours: List[str]

    def __init__(self, name: str, county_type: CountyType, neighbours):
        super().__init__(name, county_type)
        self.__neighbours = neighbours

    def determine_canonic_name(self):
        self._canonic_name = self._name

    def get_neighbours(self):
        return self.__neighbours

