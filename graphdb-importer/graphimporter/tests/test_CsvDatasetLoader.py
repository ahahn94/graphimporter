import unittest

from graphimporter.Datapoint import Datapoint
from graphimporter.CsvDatasetLoader import CsvDatasetLoader


class CsvDatasetLoaderTest(unittest.TestCase):
    __csv_dataset_loader = None

    @classmethod
    def setUpClass(cls):
        cls.__csv_dataset_loader = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        cls.__csv_dataset_loader.load_dataset()

    def test_constructor_exists(self):
        self.assertIsNot(self.__csv_dataset_loader, None)

    def test_get_datapoints_is_list(self):
        datapoints = self.__csv_dataset_loader.get_datapoints()
        self.assertIsInstance(datapoints, list)

    def test_get_datapoints_is_not_empty(self):
        datapoints = self.__csv_dataset_loader.get_datapoints()
        self.assertGreater(len(datapoints), 0)

    def test_get_datapoints_has_datapoints(self):
        datapoints = self.__csv_dataset_loader.get_datapoints()
        first_element = datapoints[0]
        self.assertIsInstance(first_element, Datapoint)


if __name__ == '__main__':
    unittest.main()
