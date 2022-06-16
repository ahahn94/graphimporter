from typing import Union

from geopandas import geopandas, GeoDataFrame
from pandas import DataFrame

from graphimporter.CountyList import CountyList
from graphimporter.ShapeCounty import ShapeCounty


class ShapefileLoader:
    __COUNTY_NAME_KEY = "GEN"
    __COUNTY_TYPE_KEY = "BEZ"
    __GEOMETRY_KEY = "geometry"

    __shapefile: Union[DataFrame, GeoDataFrame]
    __county_list: CountyList

    def __init__(self, filepath):
        self.__filepath = filepath
        self.__county_list = CountyList()

    def import_file(self):
        self.__load_shapefile()
        self.process_counties()

    def process_counties(self):
        for index, county_shape in self.__shapefile.iterrows():
            county_name = county_shape[self.__COUNTY_NAME_KEY]
            county_type = county_shape[self.__COUNTY_TYPE_KEY]
            county_neighbours = self.__identify_neighbours(county_shape)
            county = ShapeCounty(county_name, county_type, county_neighbours)
            self.__county_list.append(county)

    def __load_shapefile(self):
        self.__shapefile = geopandas.read_file(self.__filepath)

    def __identify_neighbours(self, county_shape):
        neighbours = self.__shapefile[self.__shapefile.touches(county_shape[self.__GEOMETRY_KEY])]
        names = neighbours[self.__COUNTY_NAME_KEY].tolist()
        names_without_duplicates = list(dict.fromkeys(names))
        return names_without_duplicates

    def get_county_list(self):
        return self.__county_list