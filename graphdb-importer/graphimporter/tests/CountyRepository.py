from graphimporter.CountyList import CountyList
from graphimporter.ShapefileImporter import ShapefileImporter


class CountyRepository:
    __shapefile_importer: ShapefileImporter
    __counties: CountyList = None

    def __init__(self, shapefile_importer: ShapefileImporter):
        self.__shapefile_importer = shapefile_importer

    def initialize(self):
        self.__shapefile_importer.import_file()
        self.__counties = self.__shapefile_importer.get_counties()
        return

    def is_initialized(self):
        return self.__counties is not None

    def get_county_by_canonic_name(self, canonic_name):
        if not self.is_initialized():
            raise RepositoryNotYetInitializedException
        return self.__counties.get_county_for_canonic_name(canonic_name)


class RepositoryNotYetInitializedException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
