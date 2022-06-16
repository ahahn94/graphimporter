from typing import List

from graphimporter.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.Datapoint import Datapoint
from graphimporter.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException


class DatapointRepository:

    __csv_dataset_loader: CsvDatasetLoader
    __datapoints: List[Datapoint] = None
    __county_names: List[str] = None

    def __init__(self, csv_dataset_loader: CsvDatasetLoader):
        self.__csv_dataset_loader = csv_dataset_loader

    def initialize(self):
        self.__csv_dataset_loader.load_dataset()
        self.__datapoints = self.__csv_dataset_loader.get_datapoints()
        self.__county_names = self.__collect_county_names()

    def __collect_county_names(self):
        county_names_dictionary = {}
        for datapoint in self.__datapoints:
            county_names_dictionary[datapoint.get_county()] = ""
        return list(county_names_dictionary.keys())

    def is_initialized(self):
        return self.__datapoints is not None and self.__county_names is not None

    def get_county_names(self):
        if (not self.is_initialized()):
            raise RepositoryNotYetInitializedException
        return self.__county_names