from graphimporter.entities.County import County
from graphimporter.entities.CountyType import CountyType


class DatasetCounty(County):

    def __init__(self, name: str, county_type: CountyType):
        super().__init__(name, county_type)

    def determine_canonic_name(self):
        self._canonic_name = self._name
