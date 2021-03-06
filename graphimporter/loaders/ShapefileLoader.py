from geopandas import geopandas

from graphimporter.entities.RawCounty import RawCounty
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory


class ShapefileLoader:
    __COUNTY_NAME_KEY = "GEN"
    __COUNTY_TYPE_KEY = "BEZ"
    __GEOMETRY_KEY = "geometry"

    def __init__(self, filepath, shape_county_factory: ShapeCountyFactory):
        self.__filepath = filepath
        self.__shape_county_factory = shape_county_factory
        self.__county_list = []

    def load_counties(self):
        shapes = self.__load_shapes_from_file()
        return self.__create_counties_from_shapes(shapes)

    def __create_counties_from_shapes(self, shapes):
        county_list = []
        for index, county_shape in shapes.iterrows():
            county = self.__create_county_from_shape(county_shape, shapes)
            county_list.append(county)
        return county_list

    def __create_county_from_shape(self, county_shape, shapes):
        county_name = county_shape[self.__COUNTY_NAME_KEY]
        county_type = county_shape[self.__COUNTY_TYPE_KEY]
        county_neighbours = self.__identify_neighbours(county_shape, shapes)
        county = self.__shape_county_factory.create(RawCounty(county_name, county_type), county_neighbours)
        return county

    def __load_shapes_from_file(self):
        return geopandas.read_file(self.__filepath)

    def __identify_neighbours(self, county_shape, shapes):
        neighbour_shapes = shapes[shapes.touches(county_shape[self.__GEOMETRY_KEY])]
        neighbours = []
        for county_name, county_type in zip(neighbour_shapes[self.__COUNTY_NAME_KEY],
                                            neighbour_shapes[self.__COUNTY_TYPE_KEY]):
            neighbours.append(RawCounty(county_name, county_type))
        return neighbours
