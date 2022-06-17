from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException
from graphimporter.entities.DatasetCounty import DatasetCounty
from graphimporter.repositories.DatapointRepository import DatapointRepository


class DatasetCountyRepository:
    __datapoint_repository: DatapointRepository
    __county_list = None

    def __init__(self, datapoint_repository):
        self.__datapoint_repository = datapoint_repository

    def initialize(self):
        self.__datapoint_repository.initialize()
        county_names = self.__datapoint_repository.get_county_names()
        self.__county_list = self.__create_counties_from_county_names(county_names)

    def is_initialized(self):
        return self.__county_list is not None

    def get_county_list(self):
        if not self.is_initialized():
            raise RepositoryNotYetInitializedException
        return self.__county_list

    @staticmethod
    def __create_counties_from_county_names(county_names):
        county_list = []
        for county_name in county_names:
            county_list.append(DatasetCounty(county_name, ""))
        return county_list
