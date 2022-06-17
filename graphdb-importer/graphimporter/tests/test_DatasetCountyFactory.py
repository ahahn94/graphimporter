import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.UnknownCountyTypeException import UnknownCountyTypeException
from graphimporter.entities.DatasetCounty import DatasetCounty
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory


class DatasetCountyFactoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        name_normalizer = CountyNameNormalizer()
        cls.__dataset_county_factory = DatasetCountyFactory(name_normalizer)

    def test_create_returns_dataset_county(self):
        county_name = "LK Oberbergischer Kreis"
        county = self.__dataset_county_factory.create(county_name)
        self.assertIsInstance(county, DatasetCounty)

    def test_create_raises_exception(self):
        county_name = "OK Oberbergischer Kreis"
        with (self.assertRaises(UnknownCountyTypeException)):
            county = self.__dataset_county_factory.create(county_name)


if __name__ == '__main__':
    unittest.main()
