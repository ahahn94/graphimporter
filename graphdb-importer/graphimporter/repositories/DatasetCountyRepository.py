from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException
from graphimporter.UniqueKeyCollisionException import UniqueKeyCollisionException
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.repositories.DatapointRepository import DatapointRepository


class DatasetCountyRepository:
    __dataset_county_factory: DatasetCountyFactory
    __datapoint_repository: DatapointRepository
    __county_list = None
    __county_name_index = None
    __canonic_county_name_index = None

    def __init__(self, datapoint_repository, dataset_county_factory):
        self.__datapoint_repository = datapoint_repository
        self.__dataset_county_factory = dataset_county_factory

    def initialize(self):
        self.__datapoint_repository.initialize()
        county_names = self.__datapoint_repository.get_county_names()
        self.__county_list = self.__create_counties_from_county_names(county_names)
        self.__build_indices()

    def __build_indices(self):
        self.__county_name_index = {}
        self.__canonic_county_name_index = {}
        for county in self.__county_list:
            self.__add_county_name_to_index(county)
            self.__add_canonic_county_name_to_index(county)

    def __add_canonic_county_name_to_index(self, county):
        if county.get_canonic_name() not in self.__canonic_county_name_index:
            self.__canonic_county_name_index[county.get_canonic_name()] = county
        else:
            raise UniqueKeyCollisionException("Canonic name {0} already exists!".format(county.get_canonic_name()))

    def __add_county_name_to_index(self, county):
        if county.get_name() not in self.__county_name_index:
            self.__county_name_index[county.get_name()] = county
        else:
            raise UniqueKeyCollisionException("Name {0} already exists!".format(county.get_name()))

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
