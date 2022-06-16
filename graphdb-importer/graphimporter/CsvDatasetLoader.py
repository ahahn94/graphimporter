import csv
from typing import List

from graphimporter.Datapoint import Datapoint


class CsvDatasetLoader:

    __CSV_DELIMITER = ","

    __csv_filepath: str
    __datapoints: List[Datapoint]

    def __init__(self, filepath: str):
        self.__csv_filepath = filepath

    def load_dataset(self):
        lines_from_csv_file = self.__get_lines_from_file()
        self.__create_datapoints_from_lines(lines_from_csv_file)
        return

    def __get_lines_from_file(self):
        with open(self.__csv_filepath) as file:
            reader = csv.DictReader(file, delimiter=self.__CSV_DELIMITER)
            lines = list(reader)
        return lines

    def __create_datapoints_from_lines(self, lines_from_csv_file):
        self.__datapoints = []
        for line in lines_from_csv_file:
            datapoint = self.line_to_datapoint(line)
            self.__datapoints.append(datapoint)

    @staticmethod
    def line_to_datapoint(line):
        state = line["state"]
        county = line["county"]
        age_group = line["age_group"]
        gender = line["gender"]
        date = line["date"]
        cases = line["cases"]
        deaths = line["deaths"]
        recovered = line["recovered"]
        datapoint = Datapoint(state, county, age_group, gender, date, cases, deaths, recovered)
        return datapoint

    def get_datapoints(self):
        return self.__datapoints
