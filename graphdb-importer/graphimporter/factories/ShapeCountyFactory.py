from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.exceptions.UnknownCountyTypeException import UnknownCountyTypeException
from graphimporter.entities.CountyType import CountyType
from graphimporter.entities.RawCounty import RawCounty
from graphimporter.entities.ShapeCounty import ShapeCounty


class ShapeCountyFactory:
    __COUNTY_TYPES = {"Landkreis": CountyType.LK, "Kreis": CountyType.LK, "Stadtkreis": CountyType.SK,
                      "Kreisfreie Stadt": CountyType.SK}

    __canonic_names = {}

    def __init__(self, name_normalizer: CountyNameNormalizer):
        self.__name_normalizer = name_normalizer

    def create(self, raw_county: RawCounty, neighbours: list[RawCounty]):
        canonic_name = self.__get_canonic_name(raw_county)
        county_type = self.__extract_county_type_from_type_name(raw_county.type_name)
        normalized_neighbours = self.__canonicalize_neighbours(neighbours)
        return ShapeCounty(county_type, canonic_name, normalized_neighbours)

    def __get_canonic_name(self, raw_county: RawCounty):
        if raw_county.__str__() not in self.__canonic_names:
            self.__create_and_cache_canonic_name(raw_county)
        canonic_name = self.__canonic_names[raw_county.__str__()]
        return canonic_name

    def __create_and_cache_canonic_name(self, raw_county):
        county_type = self.__extract_county_type_from_type_name(raw_county.type_name)
        raw_canonic_name = county_type.name + " " + raw_county.county_name
        canonic_name = self.__name_normalizer.normalize(raw_canonic_name)
        self.__canonic_names[raw_county.__str__()] = canonic_name

    def __extract_county_type_from_type_name(self, county_type_name: str) -> CountyType:
        if county_type_name in self.__COUNTY_TYPES:
            return self.__COUNTY_TYPES[county_type_name]
        else:
            raise UnknownCountyTypeException(county_type_name)

    def __canonicalize_neighbours(self, neighbours: list[RawCounty]):
        normalized_neighbours = []
        for neighbour in neighbours:
            normalized_neighbours.append(self.__get_canonic_name(neighbour))
        return normalized_neighbours
