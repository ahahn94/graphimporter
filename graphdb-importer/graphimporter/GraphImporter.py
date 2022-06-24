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

    def import_datasets(self):
        datapoints = self.__datapoint_repository.get_datapoints()
        last_datapoint_exists = self.__neo4j_repository.datapoint_exists(datapoints[len(datapoints) - 1])
        if not last_datapoint_exists:
            self.__datapoints_counter = 0
            self.__total_number_of_datapoints = len(datapoints)
            self.__dataset_counter_step_size = int(self.__total_number_of_datapoints / 1000)
            for datapoint in datapoints:
                self.__neo4j_repository.insert_datapoint(datapoint)
                self.__datapoints_counter += 1
                if self.__datapoints_counter % self.__dataset_counter_step_size == 0:
                    percent = self.__datapoints_counter / self.__total_number_of_datapoints * 100
                    print("Creating Datapoints... {:.1f}%".format(percent))

    def create_relations(self):
        mapped_counties = self.__mapped_county_repository.get_mapped_counties()
        self.__total_number_of_neighbours = 0
        for county in mapped_counties:
            self.__total_number_of_neighbours += len(county.get_neighbours())
        self.__neighbours_counter = 0
        self.__neighbours_counter_step_size = int(self.__total_number_of_neighbours / 1000)
        for mapped_county in mapped_counties:
            county_name = mapped_county.get_dataset_county_name()
            for neighbour in mapped_county.get_neighbours():
                neighbour_county_name = neighbour
                try:
                    self.__neighbours_counter += 1
                    neighbour_county = self.__mapped_county_repository.get_mapped_county_by_canonic_name(neighbour)
                    canonic_neighbour_county_name = neighbour_county.get_dataset_county_name()
                    self.__neo4j_repository.add_neighbour_county_relationship(county_name,
                                                                              canonic_neighbour_county_name)
                    if self.__neighbours_counter % self.__neighbours_counter_step_size == 0:
                        percent = self.__neighbours_counter / self.__total_number_of_neighbours * 100
                        print("Creating Neighbours... {:.1f}%".format(percent))
                except AttributeError as error:
                    print(f"county: {county_name}, neighbour: {neighbour_county_name}")
