import unittest

from graphimporter.mappers.CountyMapper import CountyMapper
from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.entities.MappedCounty import MappedCounty
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory
from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.loaders.ShapefileLoader import ShapefileLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository
from graphimporter.repositories.ShapeCountyRepository import ShapeCountyRepository


class CountyMapperTest(unittest.TestCase):

    __county_mapper: CountyMapper = None
    __shape_county_repository: ShapeCountyRepository = None
    __dataset_county_repository: DatasetCountyRepository = None

    @classmethod
    def setUpClass(cls):
        name_normalizer = CountyNameNormalizer()
        cls.__dataset_county_repository = cls.instantiate_dataset_county_repository(name_normalizer)
        cls.__shape_county_repository = cls.instantiate_shape_county_repository(name_normalizer)
        cls.__county_mapper = CountyMapper(cls.__dataset_county_repository, cls.__shape_county_repository)
        cls.__county_mapper.initialize()
        cls.__mapped_counties = cls.__county_mapper.map_counties()

    @classmethod
    def instantiate_shape_county_repository(cls, name_normalizer):
        shape_county_factory = ShapeCountyFactory(name_normalizer)
        shapefile_loader = ShapefileLoader("testfiles/de_county.shp", shape_county_factory)
        return ShapeCountyRepository(shapefile_loader)

    @classmethod
    def instantiate_dataset_county_repository(cls, name_normalizer):
        csv_dataset_loader = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        datapoint_repository = DatapointRepository(csv_dataset_loader)
        dataset_county_factory = DatasetCountyFactory(name_normalizer)
        return DatasetCountyRepository(datapoint_repository, dataset_county_factory)

    def test_map_counties_returns_list_of_mapped_county(self):
        self.assertEqual(type(self.__mapped_counties), type([MappedCounty]))

    def test_map_counties_returns_right_number_of_elements(self):
        number_of_dataset_counties = len(self.__dataset_county_repository.get_county_list())
        self.assertEqual(len(self.__mapped_counties), number_of_dataset_counties)


if __name__ == '__main__':
    unittest.main()
