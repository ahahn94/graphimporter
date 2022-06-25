import time

from graphimporter.CountyMapper import CountyMapper
from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory
from graphimporter.interfaces.DatabaseConnection import DatabaseConnectionInterface
from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.loaders.ShapefileLoader import ShapefileLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository
from graphimporter.repositories.MappedCountyRepository import MappedCountyRepository
from graphimporter.repositories.Neo4jRepository import Neo4jRepository
from graphimporter.repositories.ShapeCountyRepository import ShapeCountyRepository


class GraphImporter:
    __server_uri: str = None
    __username: str = None
    __password: str = None
    __path_to_shape_file: str = None
    __path_to_dataset_file: str = None

    __datapoints_counter: int
    __total_number_of_datapoints: int
    __dataset_counter_step_size: int

    __neighbours_counter: int
    __total_number_of_neighbours: int
    __neighbours_counter_step_size: int

    __csv_dataset_loader: CsvDatasetLoader
    __datapoint_repository: DatapointRepository
    __name_normalizer: CountyNameNormalizer
    __dataset_county_factory: DatasetCountyFactory
    __shape_county_factory: ShapeCountyFactory
    __shapefile_loader: ShapefileLoader
    __shape_county_repository: ShapeCountyRepository
    __dataset_county_repository: DatasetCountyRepository
    __county_mapper: CountyMapper
    __database_connection: DatabaseConnectionInterface
    __datapoint_node_mapper: DatapointNodeMapper
    __neo4j_repository: Neo4jRepository
    __mapped_county_repository: MappedCountyRepository

    def __init__(self, database_connection, path_to_dataset_file, path_to_shape_file):
        self.__database_connection = database_connection
        self.__path_to_dataset_file = path_to_dataset_file
        self.__path_to_shape_file = path_to_shape_file
        self.__initialize()

    def __initialize(self):
        print("Initializing components...")
        self.__csv_dataset_loader = CsvDatasetLoader(self.__path_to_dataset_file)
        self.__datapoint_repository = DatapointRepository(self.__csv_dataset_loader)
        self.__name_normalizer = CountyNameNormalizer()
        self.__dataset_county_factory = DatasetCountyFactory(self.__name_normalizer)
        self.__shape_county_factory = ShapeCountyFactory(self.__name_normalizer)
        self.__shapefile_loader = ShapefileLoader(self.__path_to_shape_file, self.__shape_county_factory)
        self.__shape_county_repository = ShapeCountyRepository(self.__shapefile_loader)
        self.__dataset_county_repository = DatasetCountyRepository(self.__datapoint_repository,
                                                                   self.__dataset_county_factory)
        self.__county_mapper = CountyMapper(self.__dataset_county_repository, self.__shape_county_repository)
        self.__datapoint_node_mapper = DatapointNodeMapper()
        self.__neo4j_repository = Neo4jRepository(self.__database_connection, self.__datapoint_node_mapper)
        self.__neo4j_repository.initialize()
        self.__datapoint_repository.initialize()
        self.__mapped_county_repository = MappedCountyRepository(self.__dataset_county_repository,
                                                                 self.__shape_county_repository)
        self.__mapped_county_repository.initialize()

    def import_datasets_and_relationships(self):
        start_time = time.process_time()
        self.import_datasets()
        self.create_relations()
        end_time = time.process_time()
        time_between = time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))
        print("Operations took {}".format(time_between))

    def import_datasets(self):
        datapoints = self.__datapoint_repository.get_datapoints()
        last_datapoint_exists = self.__neo4j_repository.datapoint_exists(datapoints[len(datapoints) - 1])
        if not last_datapoint_exists:
            self.__datapoints_counter = 0
            self.__total_number_of_datapoints = len(datapoints)
            self.__dataset_counter_step_size = int(self.__total_number_of_datapoints / 100)
            for datapoint in datapoints:
                self.__create_datapoint(datapoint)
            print("Completed")

    def __create_datapoint(self, datapoint):
        self.__neo4j_repository.insert_datapoint(datapoint)
        self.__datapoints_counter += 1
        self.__log_progress(self.__datapoints_counter, self.__dataset_counter_step_size,
                            self.__total_number_of_datapoints, "Creating Datapoints...")

    def create_relations(self):
        self.create_neighbour_relationships()
        self.create_gender_relationships()
        self.create_age_group_relationships()
        self.create_date_relationships()
        print("Completed.")

    def create_neighbour_relationships(self):
        mapped_counties = self.__mapped_county_repository.get_mapped_counties()
        self.__initialize_neighbour_counting(mapped_counties)
        for mapped_county in mapped_counties:
            self.__create_neighbours_for_county(mapped_county)
        self.__mesh_berlin_districts()

    def create_age_group_relationships(self):
        print("Adding Age Group Relationships")
        age_groups = ["00-04", "05-14", "15-34", "35-59", "60-79", "80-99", "NA"]
        for index, element in enumerate(age_groups):
            previous_group, current_group, next_group = self.__get_previous_current_next(age_groups, index)
            if previous_group is not None:
                self.__neo4j_repository.add_younger_relationship(previous_group, current_group)
            if next_group is not None:
                self.__neo4j_repository.add_older_relationship(next_group, current_group)

    def create_date_relationships(self):
        print("Adding Date Relationships")
        dates = self.__datapoint_repository.get_dates()
        for index, element in enumerate(dates):
            previous_day, current_day, next_day = self.__get_previous_current_next(dates, index)
            if previous_day is not None:
                self.__neo4j_repository.add_previous_day_relationship(previous_day, current_day)
            if next_day is not None:
                self.__neo4j_repository.add_next_day_relationship(next_day, current_day)

    def create_gender_relationships(self):
        print("Adding Gender Relationships...")
        self.__neo4j_repository.add_gender_relationships()

    def __get_previous_current_next(self, elements: [], index):
        previous_index = index - 1
        next_index = index + 1
        previous_element = elements[previous_index] if previous_index >= 0 else None
        current_element = elements[index] if 0 <= index <= len(elements) - 1 else None
        next_element = elements[next_index] if next_index < len(elements) - 1 else None
        return previous_element, current_element, next_element

    def __initialize_neighbour_counting(self, mapped_counties):
        self.__total_number_of_neighbours = 0
        for county in mapped_counties:
            self.__total_number_of_neighbours += len(county.get_neighbours())
        self.__neighbours_counter = 0
        self.__neighbours_counter_step_size = int(self.__total_number_of_neighbours / 100)

    def __mesh_berlin_districts(self):
        self.__neo4j_repository.add_neighbour_county_relationship("SK Berlin.*", "SK Berlin.*")

    def __create_neighbours_for_county(self, mapped_county):
        county_name = mapped_county.get_dataset_county_name()
        for neighbour in mapped_county.get_neighbours():
            self.__create_neighbour_relation(county_name, neighbour)
            self.__neighbours_counter += 1
            self.__log_progress(self.__neighbours_counter, self.__neighbours_counter_step_size,
                                self.__total_number_of_neighbours, "Creating Neighbours...")

    def __create_neighbour_relation(self, county_name, neighbour_county_name):
        if neighbour_county_name == "SK Berlin":
            # Berlin is split up into districts -> redirect to all districts.
            canonic_neighbour_county_name = "SK Berlin.*"
        elif neighbour_county_name == "SK Eisenach":
            # Eisenach isn't a county anymore.
            return
        else:
            neighbour_county = self.__mapped_county_repository.get_mapped_county_by_canonic_name(neighbour_county_name)
            canonic_neighbour_county_name = neighbour_county.get_dataset_county_name()
        self.__neo4j_repository.add_neighbour_county_relationship(county_name, canonic_neighbour_county_name)

    def __log_progress(self, counter, step_size, total, description):
        if counter % step_size == 0:
            percent = counter / total * 100
            print("{} {:.1f}%".format(description, percent))
