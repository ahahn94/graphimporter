from graphimporter.entities.DatasetCounty import DatasetCounty


class DatasetCountyFactory:

    def __init__(self, name_normalizer):
        self.__name_normalizer = name_normalizer

    def create(self, county_name):
        return DatasetCounty(county_name, "")
