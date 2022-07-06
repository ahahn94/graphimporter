from graphimporter.entities.MappedCounty import MappedCounty
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository
from graphimporter.repositories.ShapeCountyRepository import ShapeCountyRepository


class CountyMapper:

    __shape_county_repository: ShapeCountyRepository
    __dataset_county_repository: DatasetCountyRepository

    def __init__(self, dataset_county_repository: DatasetCountyRepository,
                 shape_county_repository: ShapeCountyRepository):
        self.__dataset_county_repository = dataset_county_repository
        self.__shape_county_repository = shape_county_repository

    def initialize(self):
        if not self.__dataset_county_repository.is_initialized():
            self.__dataset_county_repository.initialize()
        if not self.__shape_county_repository.is_initialized():
            self.__shape_county_repository.initialize()

    def map_counties(self):
        mapped_counties = []
        for dataset_county in self.__dataset_county_repository.get_county_list():
            shape_county = self.__shape_county_repository.get_county_by_canonic_name(dataset_county.get_canonic_name())
            mapped_counties.append(MappedCounty(dataset_county, shape_county))
        return mapped_counties
