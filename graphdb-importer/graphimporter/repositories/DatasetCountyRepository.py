from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.repositories.DatapointRepository import DatapointRepository


class DatasetCountyRepository:
    __dataset_county_factory: DatasetCountyFactory
    __datapoint_repository: DatapointRepository
    __county_list = None

    def __init__(self, datapoint_repository, dataset_county_factory):
        self.__datapoint_repository = datapoint_repository
        self.__dataset_county_factory = dataset_county_factory

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

    def __create_counties_from_county_names(self, county_names):
        county_list = []
        for county_name in county_names:
            dataset_county = self.__dataset_county_factory.create(county_name)
            county_list.append(dataset_county)
        return county_list
