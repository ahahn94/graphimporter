import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.entities.NoSuchCountyException import NoSuchCountyException
from graphimporter.entities.ShapeCounty import ShapeCounty
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory
from graphimporter.loaders.ShapefileLoader import ShapefileLoader
from graphimporter.repositories.ShapeCountyRepository import ShapeCountyRepository
from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException


class ShapeCountyRepositoryTest(unittest.TestCase):
    __shapefile_loader = None
    __shape_county_repository = None

    @classmethod
    def setUpClass(cls):
        name_normalizer = CountyNameNormalizer()
        shape_county_factory = ShapeCountyFactory(name_normalizer)
        cls.__shapefile_loader = ShapefileLoader("testfiles/de_county.shp", shape_county_factory)
        cls.__shape_county_repository = ShapeCountyRepository(cls.__shapefile_loader)
        cls.__shape_county_repository.initialize()

    def test_is_initialized(self):
        self.assertEqual(self.__shape_county_repository.is_initialized(), True)

    def test_get_county_by_canonic_name_returns_county(self):
        county = self.__shape_county_repository.get_county_by_canonic_name("SK Flensburg")
        self.assertIsInstance(county, ShapeCounty)

    def test_get_county_by_canonic_name_not_found(self):
        with (self.assertRaises(NoSuchCountyException)):
            self.__shape_county_repository.get_county_by_canonic_name("Flänsburg")

    def test_get_county_by_canonic_name_uninitialized(self):
        shape_county_repository = ShapeCountyRepository(self.__shapefile_loader)
        with (self.assertRaises(RepositoryNotYetInitializedException)):
            shape_county_repository.get_county_by_canonic_name("Flänsburg")


if __name__ == '__main__':
    unittest.main()
