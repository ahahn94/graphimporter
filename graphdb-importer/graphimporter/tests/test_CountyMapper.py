import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.entities.NoSuchCountyException import NoSuchCountyException
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository
from graphimporter.repositories.ShapeCountyRepository import ShapeCountyRepository
from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.loaders.ShapefileLoader import ShapefileLoader


class CountyMapperTest(unittest.TestCase):

    __shape_county_repository = None
    __dataset_county_repository = None

    @classmethod
    def setUpClass(cls):
        name_normalizer = CountyNameNormalizer()
        cls.__dataset_county_repository = cls.instantiate_dataset_county_repository(name_normalizer)
        cls.__dataset_county_repository.initialize()
        cls.__shape_county_repository = cls.instantiate_shape_county_repository(name_normalizer)
        cls.__shape_county_repository.initialize()

    @classmethod
    def instantiate_shape_county_repository(cls, name_normalizer):
        shape_county_factory = ShapeCountyFactory(name_normalizer)
        shapefile_loader = ShapefileLoader("testfiles/de_county.shp", shape_county_factory)
        return ShapeCountyRepository(shapefile_loader)

    @classmethod
    def instantiate_dataset_county_repository(cls, name_normalizer):
        csv_dataset_loader = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        datapoint_repository = DatapointRepository(csv_dataset_loader)
        dataset_county_factory = DatasetCountyFactory(name_normalizer)
        return DatasetCountyRepository(datapoint_repository, dataset_county_factory)

    def test_mapping(self):
        exception_counter = 0
        for county in self.__dataset_county_repository.get_county_list():
            try:
                self.__shape_county_repository.get_county_by_canonic_name(county.get_canonic_name())
            except NoSuchCountyException:
                if "Berlin" not in county.get_canonic_name():
                    exception_counter += 1
        self.assertEqual(exception_counter, 0)

if __name__ == '__main__':
    unittest.main()
