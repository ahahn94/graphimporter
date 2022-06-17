from graphimporter.entities.ShapeCounty import ShapeCounty


class ShapeCountyFactory:

    def __init__(self, name_normalizer):
        self.__name_normalizer = name_normalizer

    def create(self, county_name, county_type, neighbours):
        return ShapeCounty(county_name, county_type, neighbours)