from graphimporter.UnknownCountyTypeException import UnknownCountyTypeException
from graphimporter.entities.CountyType import CountyType
from graphimporter.entities.ShapeCounty import ShapeCounty


class ShapeCountyFactory:
    __county_types = {"Landkreis": CountyType.LK, "Kreis": CountyType.LK, "Stadtkreis": CountyType.SK, "Kreisfreie Stadt": CountyType.SK}

    def __init__(self, name_normalizer):
        self.__name_normalizer = name_normalizer

    def create(self, county_name: str, county_type_name: str, neighbours):
        county_type = self.__extract_county_type_from_type_name(county_type_name)
        return ShapeCounty(county_name, county_type, neighbours)

    def __extract_county_type_from_type_name(self, county_type_name: str) -> CountyType:
        if county_type_name in self.__county_types:
            return self.__county_types[county_type_name]
        else:
            raise UnknownCountyTypeException(county_type_name)
