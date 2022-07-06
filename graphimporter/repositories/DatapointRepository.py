from typing import List

from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.entities.Datapoint import Datapoint
from graphimporter.exceptions.RepositoryNotYetInitializedException import RepositoryNotYetInitializedException


class DatapointRepository:
    __csv_dataset_loader: CsvDatasetLoader
    __datapoints: List[Datapoint] = None
    __counties_and_states: {} = None
    __dates: List[str] = None
    __age_groups: List[str] = None
    __genders: List[str] = None
    __datapoints_index: {} = None

    def __init__(self, csv_dataset_loader: CsvDatasetLoader):
        self.__csv_dataset_loader = csv_dataset_loader

    def initialize(self):
        self.__csv_dataset_loader.load_dataset()
        self.__datapoints = self.__csv_dataset_loader.get_datapoints()
        self.__counties_and_states = self.__collect_counties_and_states()
        self.__dates = self.__collect_dates()
        self.__age_groups = self.__collect_age_groups()
        self.__genders = self.__collect_genders()
        self.__build_index_and_create_missing_datapoints()

    def __collect_counties_and_states(self):
        counties_and_states = {}
        for datapoint in self.__datapoints:
            counties_and_states[datapoint.get_county()] = datapoint.get_state()
        return counties_and_states

    def __collect_county_names(self):
        county_names_dictionary = {}
        for datapoint in self.__datapoints:
            county_names_dictionary[datapoint.get_county()] = ""
        return list(county_names_dictionary.keys())

    def __collect_dates(self):
        dates_dictionary = {}
        for datapoint in self.__datapoints:
            dates_dictionary[datapoint.get_date()] = ""
        return sorted(list(dates_dictionary))

    def __collect_age_groups(self):
        age_groups_dictionary = {}
        for datapoint in self.__datapoints:
            age_groups_dictionary[datapoint.get_age_group()] = ""
        return sorted(list(age_groups_dictionary))

    def __collect_genders(self):
        genders_dictionary = {}
        for datapoint in self.__datapoints:
            genders_dictionary[datapoint.get_gender()] = ""
        return sorted(list(genders_dictionary))

    def __build_index_and_create_missing_datapoints(self):
        self.__build_index_of_empty_datapoints()
        self.__replace_existing_datapoints_into_index()
        self.__datapoints = list(self.__datapoints_index.values())

    def __replace_existing_datapoints_into_index(self):
        for datapoint in self.__datapoints:
            self.__datapoints_index[datapoint.identifiers_string()] = datapoint

    def __build_index_of_empty_datapoints(self):
        self.__datapoints_index = {}
        for county, state in self.__counties_and_states.items():
            for age_group in self.__age_groups:
                for date in self.__dates:
                    for gender in self.__genders:
                        datapoint = Datapoint(state, county, age_group, gender, date, 0, 0, 0)
                        identifiers_string = datapoint.identifiers_string
                        self.__datapoints_index[identifiers_string()] = datapoint

    def is_initialized(self):
        return self.__datapoints is not None and self.__counties_and_states is not None and self.__dates is not None

    def get_county_names(self):
        if not self.is_initialized():
            raise RepositoryNotYetInitializedException
        return list(self.__counties_and_states.keys())

    def get_datapoints(self):
        return self.__datapoints

    def get_dates(self):
        return self.__dates
