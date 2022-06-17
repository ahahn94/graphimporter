import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.entities.ShapeCounty import ShapeCounty
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory


class ShapeCountyFactoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        name_normalizer = CountyNameNormalizer()
        cls.__shape_county_factory = ShapeCountyFactory(name_normalizer)

    def test_create_county_returns_shape_county(self):
        county_name = "Oberbergischer Kreis"
        county_type = "Kreis"
        county_neighbours = ['Remscheid', 'Wuppertal', 'Rheinisch-Bergischer Kreis', 'Rhein-Sieg-Kreis', 'Ennepe-Ruhr-Kreis', 'Märkischer Kreis', 'Olpe', 'Altenkirchen (Westerwald)']
        shape_county = self.__shape_county_factory.create(county_name, county_type, county_neighbours)
        self.assertIsInstance(shape_county, ShapeCounty)


if __name__ == '__main__':
    unittest.main()
