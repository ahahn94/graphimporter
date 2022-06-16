import unittest

from graphimporter.CountyList import NoSuchCountyException
from graphimporter.ShapeCounty import ShapeCounty
from graphimporter.ShapefileLoader import ShapefileLoader
from graphimporter.CountyRepository import CountyRepository
from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException


class CountyRepositoryTest(unittest.TestCase):
    __shapefile_loader = None
    __county_repository = None

    @classmethod
    def setUpClass(cls):
        cls.__shapefile_loader = ShapefileLoader("testfiles/de_county.shp")
        cls.__county_repository = CountyRepository(cls.__shapefile_loader)
        cls.__county_repository.initialize()

    def test_is_initialized(self):
        self.assertEqual(self.__county_repository.is_initialized(), True)

    def test_get_county_by_canonic_name_returns_county(self):
        county = self.__county_repository.get_county_by_canonic_name("Flensburg")
        self.assertIsInstance(county, ShapeCounty)

    def test_get_county_by_canonic_name_not_found(self):
        with (self.assertRaises(NoSuchCountyException)):
            self.__county_repository.get_county_by_canonic_name("Flänsburg")

    def test_get_county_by_canonic_name_uninitialized(self):
        county_repository = CountyRepository(self.__shapefile_loader)
        with (self.assertRaises(RepositoryNotYetInitializedException)):
            county_repository.get_county_by_canonic_name("Flänsburg")


if __name__ == '__main__':
    unittest.main()
