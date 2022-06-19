from graphimporter.CountyMapper import CountyMapper
from graphimporter.entities.MappedCounty import MappedCounty
from graphimporter.exceptions.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException


class MappedCountyRepository:
    __mapped_counties: [MappedCounty] = None

    def __init__(self, dataset_county_repository, shape_county_repository):
        self.__dataset_county_repository = dataset_county_repository
        self.__shape_county_repository = shape_county_repository
        self.__county_mapper = CountyMapper(self.__dataset_county_repository, self.__shape_county_repository)

    def initialize(self):
        self.__county_mapper.initialize()
        self.__mapped_counties = self.__county_mapper.map_counties()

    def is_initialized(self):
        return self.__mapped_counties is not None

    def get_mapped_counties(self):
        if self.is_initialized():
            return self.__mapped_counties
        else:
            raise RepositoryNotYetInitializedException
