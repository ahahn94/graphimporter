import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer


class CountyNameNormalizerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__county_name_normalizer = CountyNameNormalizer()

    def test_replace_umlaute_lower_case(self):
        test_input = "übergrößengeschäft"
        expected = "uebergroessengeschaeft"
        result = self.__county_name_normalizer.normalize(test_input)
        self.assertEqual(result, expected)

    def test_replace_umlaute_upper_case(self):
        test_input = "ÜBERGRÖẞENGESCHÄFT"
        expected = "UEBERGROESSENGESCHAEFT"
        result = self.__county_name_normalizer.normalize(test_input)
        self.assertEqual(result, expected)

    def test_replace_prepositions(self):
        test_input = "am Main, a. Main, an der Oder, a.d. Oder, im Breisgau, i. Breisgau, in der Pfalz, i.d. Pfalz"
        expected = "a.Main, a.Main, a.d.Oder, a.d.Oder, i.Breisgau, i.Breisgau, i.d.Pfalz, i.d.Pfalz"
        result = self.__county_name_normalizer.normalize(test_input)
        self.assertEqual(result, expected)

    def test_replace_text_in_brackets(self):
        test_input = "Frankfurt (Oder)"
        expected = "Frankfurt"
        result = self.__county_name_normalizer.normalize(test_input)
        self.assertEqual(result, expected)

    def test_strip_whitespaces(self):
        test_input = " Frankfurt "
        expected = "Frankfurt"
        result = self.__county_name_normalizer.normalize(test_input)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
