import unittest

from graphimporter.UnmergeableCountiesException import UnmergeableCountiesException
from graphimporter.entities.CountyType import CountyType
from graphimporter.entities.ShapeCounty import ShapeCounty


class ShapeCountyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__flensburg_1 = ShapeCounty("Flensburg", CountyType.SK, "Flensburg", ['Flensburg', 'Schleswig-Flensburg'])
        cls.__flensburg_2 = ShapeCounty("Flensburg", CountyType.SK, "Flensburg", ['Schleswig-Flensburg', 'Flensburg'])
        cls.__pinneberg_1 = ShapeCounty("Pinneberg", CountyType.LK, "LK Pinneberg", ['Pinneberg', 'Stade'])
        cls.__pinneberg_2 = ShapeCounty("Pinneberg", CountyType.LK, "LK Pinneberg",
                                        ['Pinneberg', 'Steinburg', 'Hamburg'])
        cls.__pinneberg_complete = ShapeCounty("Pinneberg", CountyType.LK, "LK Pinneberg",
                                               ['Pinneberg', 'Steinburg', 'Hamburg', 'Stade'])

    def test_compare_match(self):
        self.assertEqual(self.__flensburg_1.same_county(self.__flensburg_2), True)

    def test_compare_mismatch(self):
        self.assertEqual(self.__flensburg_1.same_county(self.__pinneberg_complete), False)

    def test_merge_match(self):
        result = self.__pinneberg_1.merge(self.__pinneberg_2)
        self.assertEqual(result.equals(self.__pinneberg_complete), True)

    def test_merge_mismatch_raises_exception(self):
        with (self.assertRaises(UnmergeableCountiesException)):
            self.__pinneberg_1.merge(self.__flensburg_1)


if __name__ == '__main__':
    unittest.main()
