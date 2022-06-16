from graphimporter.CountyList import CountyList
from graphimporter.ShapefileLoader import ShapefileLoader


class CountyRepository:
    __shapefile_loader: ShapefileLoader
    __county_list: CountyList = None

    def __init__(self, shapefile_loader: ShapefileLoader):
        self.__shapefile_loader = shapefile_loader

    def initialize(self):
        self.__county_list = self.__shapefile_loader.load_counties()

    def is_initialized(self):
        return self.__county_list is not None

    def get_county_by_canonic_name(self, canonic_name):
        if not self.is_initialized():
            raise RepositoryNotYetInitializedException
        return self.__county_list.get_county_for_canonic_name(canonic_name)


class RepositoryNotYetInitializedException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
