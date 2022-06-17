from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.UnknownCountyTypeException import UnknownCountyTypeException
from graphimporter.entities.CountyType import CountyType
from graphimporter.entities.DatasetCounty import DatasetCounty


class DatasetCountyFactory:

    __county_types = {"SK": CountyType.SK, "LK": CountyType.LK, "Region": CountyType.LK, "StaedteRegion": CountyType.LK}

    def __init__(self, name_normalizer: CountyNameNormalizer):
        self.__name_normalizer = name_normalizer

    def create(self, county_name: str):
        county_type = self.__extract_county_type_from_name(county_name)
        canonic_name = self.__name_normalizer.normalize(county_name)
        return DatasetCounty(county_name, county_type, canonic_name)

    def __extract_county_type_from_name(self, county_name: str) -> CountyType:
        raw_county_type = county_name.split(" ", 1)[0]
        if raw_county_type in self.__county_types:
            return self.__county_types[raw_county_type]
        else:
            raise UnknownCountyTypeException(raw_county_type)
