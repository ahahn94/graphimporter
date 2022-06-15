from typing import List

from County import County


class ShapeCounty(County):

    __neighbours: List[str]

    def __init__(self, name: str, type: str, neighbours):
        super().__init__(name, type)
        self.__neighbours = neighbours

    def determine_canonic_name(self):
        self._canonic_name = self._name

    def get_neighbours(self):
        return self.__neighbours

