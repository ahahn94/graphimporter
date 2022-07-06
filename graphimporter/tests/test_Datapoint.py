import unittest

from graphimporter.entities.Datapoint import Datapoint


class DatapointTest(unittest.TestCase):
    __datapoint: Datapoint

    @classmethod
    def setUpClass(cls):
        cls.__datapoint = Datapoint("Baden-Wuerttemberg", "LK Alb-Donau-Kreis", "00-04", "F", "2022-01-04", 1, 0, 1)

    def test_get_age_group(self):
        age_group = self.__datapoint.get_age_group()
        self.assertIsInstance(age_group, str)

    def test_get_cases(self):
        cases = self.__datapoint.get_cases()
        self.assertIsInstance(cases, int)

    def test_get_county(self):
        county = self.__datapoint.get_county()
        self.assertIsInstance(county, str)

    def test_get_date(self):
        date = self.__datapoint.get_date()
        self.assertIsInstance(date, str)

    def test_get_deaths(self):
        deaths = self.__datapoint.get_deaths()
        self.assertIsInstance(deaths, int)

    def test_get_gender(self):
        gender = self.__datapoint.get_gender()
        self.assertIsInstance(gender, str)

    def test_get_recovered(self):
        recovered = self.__datapoint.get_recovered()
        self.assertIsInstance(recovered, int)

    def test_get_state(self):
        state = self.__datapoint.get_state()
        self.assertIsInstance(state, str)


if __name__ == '__main__':
    unittest.main()
