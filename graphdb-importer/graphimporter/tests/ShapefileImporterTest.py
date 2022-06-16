import unittest

from graphimporter.CountyList import CountyList
from graphimporter.ShapefileImporter import ShapefileImporter


class ShapefileImporterTest(unittest.TestCase):
    shapefile_importer = None

    @classmethod
    def setUpClass(cls):
        cls.shapefile_importer = ShapefileImporter("testfiles/de_county.shp")
        cls.shapefile_importer.import_file()

    def testGetCountiesIsCountyList(self):
        counties = self.shapefile_importer.get_counties()
        self.assertIsInstance(counties, CountyList)

    def testGetCountiesNotEmpty(self):
        counties = self.shapefile_importer.get_counties()
        self.assertIs(counties.empty(), False)

    def testCountiesListHasCounty(self):
        counties = self.shapefile_importer.get_counties()
        counties.get_county_for_canonic_name("Oberbergischer Kreis")

    def testShapeCountiesHaveNeighbours(self):
        counties = self.shapefile_importer.get_counties()
        firstCounty = counties.get(0)
        self.assertGreater(len(firstCounty.get_neighbours()), 0)


if __name__ == '__main__':
    unittest.main()
