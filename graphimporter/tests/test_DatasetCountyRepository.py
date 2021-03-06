import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.exceptions.UniqueKeyCollisionException import UniqueKeyCollisionException
from graphimporter.entities.TypedCounty import TypedCounty
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository


class DatasetCountyRepositoryTest(unittest.TestCase):

    __dataset_county_repository: DatasetCountyRepository = None

    @classmethod
    def setUpClass(cls):
        csv_dataset_loader = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        datapoint_repository = DatapointRepository(csv_dataset_loader)
        name_normalizer = CountyNameNormalizer()
        dataset_county_factory = DatasetCountyFactory(name_normalizer)
        cls.__dataset_county_repository = DatasetCountyRepository(datapoint_repository, dataset_county_factory)
        cls.__dataset_county_repository.initialize()

    def test_get_county_list_is_list_of_county(self):
        county_list = self.__dataset_county_repository.get_county_list()
        self.assertEqual(type(county_list), type([TypedCounty]))

    def test_get_county_list_is_not_empty(self):
        county_list = self.__dataset_county_repository.get_county_list()
        self.assertGreater(len(county_list), 0)

    def test_initialize_raises_exception_on_name_collision(self):
        csv_dataset_loader = CsvDatasetLoader("testfiles/canonic_name_collisions.csv")
        datapoint_repository = DatapointRepository(csv_dataset_loader)
        name_normalizer = CountyNameNormalizer()
        dataset_county_factory = DatasetCountyFactory(name_normalizer)
        dataset_county_repository = DatasetCountyRepository(datapoint_repository, dataset_county_factory)
        with (self.assertRaises(UniqueKeyCollisionException)):
            dataset_county_repository.initialize()


if __name__ == '__main__':
    unittest.main()
