import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.entities.ShapeCounty import ShapeCounty
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

    def test_get_county_list_is_list_of_counties(self):
        self.assertEqual(type(self.__county_list), type([ShapeCounty]))

    def test_get_county_list_not_empty(self):
        self.assertGreater(len(self.__county_list), 0)

    def test_county_has_neighbours(self):
        first_county = self.__county_list[0]
        self.assertGreater(len(first_county.get_neighbours()), 0)


if __name__ == '__main__':
    unittest.main()
