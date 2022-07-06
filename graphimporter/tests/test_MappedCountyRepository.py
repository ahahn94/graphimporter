import unittest

from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.entities.MappedCounty import MappedCounty
from graphimporter.exceptions.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory
from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.loaders.ShapefileLoader import ShapefileLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository
from graphimporter.repositories.MappedCountyRepository import MappedCountyRepository
from graphimporter.repositories.ShapeCountyRepository import ShapeCountyRepository


class MappedCountyRepositoryTest(unittest.TestCase):
    __mapped_county_repository: MappedCountyRepository

    @classmethod
    def get_new_mapped_county_repository(cls):
        county_name_normalizer = CountyNameNormalizer()
        csv_dataset_loader = CsvDatasetLoader("testfiles/covid_de_testing.csv")
        datapoint_repository = DatapointRepository(csv_dataset_loader)
        dataset_county_factory = DatasetCountyFactory(county_name_normalizer)
        dataset_county_repository = DatasetCountyRepository(datapoint_repository, dataset_county_factory)
        shape_county_factory = ShapeCountyFactory(county_name_normalizer)
        shapefile_loader = ShapefileLoader("testfiles/de_county.shp", shape_county_factory)
        shape_county_repository = ShapeCountyRepository(shapefile_loader)
        mapped_county_repository = MappedCountyRepository(dataset_county_repository, shape_county_repository)
        return mapped_county_repository

    def test_get_mapped_counties_raises_exception(self):
        mapped_county_repository = self.get_new_mapped_county_repository()
        with(self.assertRaises(RepositoryNotYetInitializedException)):
            mapped_county_repository.get_mapped_counties()

    def test_get_mapped_counties_returns_mapped_counties_list(self):
        mapped_county_repository = self.get_new_mapped_county_repository()
        mapped_county_repository.initialize()
        mapped_counties = mapped_county_repository.get_mapped_counties()
        self.assertEqual(type(mapped_counties), type([MappedCounty]))


if __name__ == '__main__':
    unittest.main()
