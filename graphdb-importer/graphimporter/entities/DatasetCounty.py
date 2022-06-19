from graphimporter.entities.TypedCounty import TypedCounty
from graphimporter.entities.CountyType import CountyType


class DatasetCounty(TypedCounty):
    __name: str

    def __init__(self, name: str, county_type: CountyType, canonic_name: str):
        super().__init__(county_type, canonic_name)
        self.__name = name

    def get_name(self):
        return self.__name
