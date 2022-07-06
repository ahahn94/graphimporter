import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.exceptions.UnknownCountyTypeException import UnknownCountyTypeException
from graphimporter.entities.RawCounty import RawCounty
from graphimporter.entities.ShapeCounty import ShapeCounty
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory


class ShapeCountyFactoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        name_normalizer = CountyNameNormalizer()
        cls.__shape_county_factory = ShapeCountyFactory(name_normalizer)
        cls.__county_name = "Oberbergischer Kreis"
        cls.__county_type = "Kreis"
        cls.__county_neighbours = [
            RawCounty("Remscheid", "Kreisfreie Stadt"),
            RawCounty("Wuppertal", "Kreisfreie Stadt"),
            RawCounty("Rheinisch-Bergischer Kreis", "Kreis"),
            RawCounty("Rhein-Sieg-Kreis", "Kreis"),
            RawCounty("Ennepe-Ruhr-Kreis", "Kreis"),
            RawCounty("Märkischer Kreis", "Kreis"),
            RawCounty("Olpe", "Kreis"),
            RawCounty("Altenkirchen (Westerwald)", "Landkreis")
        ]

    def test_create_returns_shape_county(self):
        shape_county = self.__shape_county_factory.create(RawCounty(self.__county_name, self.__county_type),
                                                          self.__county_neighbours)
        self.assertIsInstance(shape_county, ShapeCounty)

    def test_create_raises_exception(self):
        county_type = "Städteregion"
        with (self.assertRaises(UnknownCountyTypeException)):
            self.__shape_county_factory.create(RawCounty(self.__county_name, county_type), self.__county_neighbours)

    def test_create_returns_county_with_canonic_neighbour_names(self):
        shape_county = self.__shape_county_factory.create(RawCounty(self.__county_name, self.__county_type),
                                                          self.__county_neighbours)
        self.assertIn("LK Olpe", shape_county.get_neighbours())


if __name__ == '__main__':
    unittest.main()
