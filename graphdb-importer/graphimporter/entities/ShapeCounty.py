from typing import List

from graphimporter.entities.County import County
from graphimporter.entities.CountyType import CountyType


class ShapeCounty(County):

    __neighbours: List[str]

    def __init__(self, name: str, county_type: CountyType, canonic_name: str, neighbours):
        super().__init__(name, county_type, canonic_name)
        self.__neighbours = neighbours

    def get_neighbours(self):
        return self.__neighbours

