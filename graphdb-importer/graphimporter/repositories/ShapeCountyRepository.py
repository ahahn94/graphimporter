import json

from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException
from graphimporter.entities.NoSuchCountyException import NoSuchCountyException
from graphimporter.entities.ShapeCounty import ShapeCounty
from graphimporter.loaders.ShapefileLoader import ShapefileLoader


class ShapeCountyRepository:
    __shapefile_loader: ShapefileLoader
    __county_list: [ShapeCounty] = None
    __county_name_index = None
    __canonic_county_name_index = None

    def __init__(self, shapefile_loader: ShapefileLoader):
        self.__shapefile_loader = shapefile_loader

    def initialize(self):
        self.__county_list = self.__shapefile_loader.load_counties()
        self.__build_indices()

    def __build_indices(self):
        self.__county_name_index = {}
        self.__canonic_county_name_index = {}
        for county in self.__county_list:
            self.__county_name_index[county.get_name()] = county
            self.__canonic_county_name_index[county.get_canonic_name()] = county

    def is_initialized(self):
        return self.__county_list is not None

    def get_county_by_canonic_name(self, canonic_name):
        if not self.is_initialized():
            raise RepositoryNotYetInitializedException
        if canonic_name in self.__canonic_county_name_index:
            return self.__canonic_county_name_index.get(canonic_name)
        else:
            raise NoSuchCountyException(canonic_name)
