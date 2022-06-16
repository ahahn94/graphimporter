import unittest

from graphimporter.Datapoint import Datapoint
from graphimporter.CsvDatasetLoader import CsvDatasetLoader


class CsvDatasetLoaderTest(unittest.TestCase):
    _datasets_importer = None

    @classmethod
    def setUpClass(cls):
        cls._datasets_importer = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        cls._datasets_importer.import_datasets()

    def test_constructor_exists(self):
        self.assertIsNot(self._datasets_importer, None)

    def test_get_datapoints_is_list(self):
        datapoints = self._datasets_importer.get_datapoints()
        self.assertIsInstance(datapoints, list)

    def test_get_datapoints_is_not_empty(self):
        datapoints = self._datasets_importer.get_datapoints()
        self.assertGreater(len(datapoints), 0)

    def test_get_datapoints_has_datapoints(self):
        datapoints = self._datasets_importer.get_datapoints()
        first_element = datapoints[0]
        self.assertIsInstance(first_element, Datapoint)


if __name__ == '__main__':
    unittest.main()
