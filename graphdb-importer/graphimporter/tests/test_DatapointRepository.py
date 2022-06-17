import unittest

from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException


class DatapointRepositoryTest(unittest.TestCase):
    __datapoint_repository: DatapointRepository
    __csv_dataset_loader: CsvDatasetLoader

    @classmethod
    def setUpClass(cls):
        cls.__csv_dataset_loader = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        cls.__datapoint_repository = DatapointRepository(cls.__csv_dataset_loader)
        cls.__datapoint_repository.initialize()

    def test_is_initialized(self):
        self.assertEqual(self.__datapoint_repository.is_initialized(), True)

    def test_get_county_names_not_empty(self):
        county_names = self.__datapoint_repository.get_county_names()
        self.assertGreater(len(county_names), 0)

    def test_get_county_names_uninitialized(self):
        datapoint_repository = DatapointRepository(self.__csv_dataset_loader)
        with (self.assertRaises(RepositoryNotYetInitializedException)):
            datapoint_repository.get_county_names()

if __name__ == '__main__':
    unittest.main()
