from graphimporter.entities.County import County
from graphimporter.entities.CountyType import CountyType


class DatasetCounty(County):

    def __init__(self, name: str, county_type: CountyType, canonic_name: str):
        super().__init__(name, county_type, canonic_name)
