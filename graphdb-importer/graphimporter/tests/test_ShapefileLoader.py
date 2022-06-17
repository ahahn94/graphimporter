import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.entities.CountyList import CountyList
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory
from graphimporter.loaders.ShapefileLoader import ShapefileLoader


class ShapefileLoaderTest(unittest.TestCase):
    __county_list = None

    @classmethod
    def setUpClass(cls):
        name_normalizer = CountyNameNormalizer()
        shape_county_factory = ShapeCountyFactory(name_normalizer)
        shapefile_loader = ShapefileLoader("testfiles/de_county.shp", shape_county_factory)
        cls.__county_list = shapefile_loader.load_counties()

    def test_get_county_list_is_county_list(self):
        self.assertIsInstance(self.__county_list, CountyList)

    def test_get_county_list_not_empty(self):
        self.assertIs(self.__county_list.empty(), False)

    def test_get_county_for_canonic_name_has_county(self):
        self.__county_list.get_county_for_canonic_name("Oberbergischer Kreis")

    def test_county_has_neighbours(self):
        firstCounty = self.__county_list.get(0)
        self.assertGreater(len(firstCounty.get_neighbours()), 0)


if __name__ == '__main__':
    unittest.main()
