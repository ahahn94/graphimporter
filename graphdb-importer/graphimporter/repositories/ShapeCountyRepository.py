from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException
from graphimporter.UniqueKeyCollisionException import UniqueKeyCollisionException
from graphimporter.entities.NoSuchCountyException import NoSuchCountyException
from graphimporter.entities.ShapeCounty import ShapeCounty
from graphimporter.loaders.ShapefileLoader import ShapefileLoader


class ShapeCountyRepository:
    __shapefile_loader: ShapefileLoader
    __county_list: [ShapeCounty] = None
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
            try:
                self.__add_county_name_to_index(county)
                self.__add_canonic_county_name_to_index(county)
            except UniqueKeyCollisionException as exception:
                print(exception.__str__())

    def __add_canonic_county_name_to_index(self, county):
        if county.get_canonic_name() not in self.__canonic_county_name_index:
            self.__canonic_county_name_index[county.get_canonic_name()] = county
        else:
            raise UniqueKeyCollisionException("Canonic name {0} already exists!".format(county.get_canonic_name()), county.__str__(), self.__canonic_county_name_index[county.get_canonic_name()].__str__())

    def __add_county_name_to_index(self, county):
        if county.get_name() not in self.__county_name_index:
            self.__county_name_index[county.get_name()] = county
        else:
            print("Merging counties")
            indexed_county = self.__county_name_index.get(county.get_name())
            print("Indexed county: " + indexed_county.__str__())
            print("Other county:" + county.__str__())
            merged_county = indexed_county.merge(county)
            print("Merged county: " + merged_county.__str__())
            self.__county_name_index[county.get_name()] = merged_county

    def is_initialized(self):
        return self.__county_list is not None

    def get_county_by_canonic_name(self, canonic_name):
        if not self.is_initialized():
            raise RepositoryNotYetInitializedException
        if canonic_name in self.__canonic_county_name_index:
            return self.__canonic_county_name_index.get(canonic_name)
        else:
            raise NoSuchCountyException(canonic_name)
