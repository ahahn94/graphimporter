import unittest

from graphimporter.entities.County import County
from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository


class DatasetCountyRepositoryTest(unittest.TestCase):

    __dataset_county_repository: DatasetCountyRepository = None

    @classmethod
    def setUpClass(cls):
        csv_dataset_loader = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        datapoint_repository = DatapointRepository(csv_dataset_loader)
        cls.__dataset_county_repository = DatasetCountyRepository(datapoint_repository)
        cls.__dataset_county_repository.initialize()

    def test_get_county_list_is_list_of_county(self):
        county_list = self.__dataset_county_repository.get_county_list()
        self.assertEqual(type(county_list), type([County]))

    def test_get_county_list_is_not_empty(self):
        county_list = self.__dataset_county_repository.get_county_list()
        self.assertGreater(len(county_list), 0)


if __name__ == '__main__':
    unittest.main()
