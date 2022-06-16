import unittest

from graphimporter.CountyList import CountyList
from graphimporter.ShapefileLoader import ShapefileLoader


class ShapefileLoaderTest(unittest.TestCase):
    shapefile_loader = None

    @classmethod
    def setUpClass(cls):
        cls.shapefile_loader = ShapefileLoader("testfiles/de_county.shp")
        cls.shapefile_loader.import_file()

    def test_get_county_list_is_county_list(self):
        county_list = self.shapefile_loader.get_county_list()
        self.assertIsInstance(county_list, CountyList)

    def test_get_county_list_not_empty(self):
        county_list = self.shapefile_loader.get_county_list()
        self.assertIs(county_list.empty(), False)

    def test_get_county_for_canonic_name_has_county(self):
        county_list = self.shapefile_loader.get_county_list()
        county_list.get_county_for_canonic_name("Oberbergischer Kreis")

    def test_county_has_neighbours(self):
        county_list = self.shapefile_loader.get_county_list()
        firstCounty = county_list.get(0)
        self.assertGreater(len(firstCounty.get_neighbours()), 0)


if __name__ == '__main__':
    unittest.main()
