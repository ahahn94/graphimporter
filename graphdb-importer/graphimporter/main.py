from graphimporter.CountyMapper import CountyMapper
from graphimporter.CountyNameNormalizer import CountyNameNormalizer
from graphimporter.Neo4jDatabaseConnection import Neo4jDatabaseConnection
from graphimporter.factories.DatasetCountyFactory import DatasetCountyFactory
from graphimporter.factories.ShapeCountyFactory import ShapeCountyFactory
from graphimporter.loaders.CsvDatasetLoader import CsvDatasetLoader
from graphimporter.loaders.ShapefileLoader import ShapefileLoader
from graphimporter.repositories.DatapointRepository import DatapointRepository
from graphimporter.repositories.DatasetCountyRepository import DatasetCountyRepository
from graphimporter.repositories.MappedCountyRepository import MappedCountyRepository
from graphimporter.repositories.Neo4jRepository import Neo4jRepository
from graphimporter.repositories.ShapeCountyRepository import ShapeCountyRepository


def import_datasets():
    neo4j_database_connection = Neo4jDatabaseConnection(__server_uri, __username, __password)
    neo4j_repository = Neo4jRepository(neo4j_database_connection)
    neo4j_repository.initialize()
    datapoint_repository.initialize()
    datapoints = datapoint_repository.get_datapoints()
    total = len(datapoints)
    counter = 0
    for datapoint in datapoints:
        neo4j_repository.insert_datapoint(datapoint)
        counter += 1
        print(counter.__str__() + "/" + total.__str__())


def create_relations():
    mapped_county_repository = MappedCountyRepository(dataset_county_repository, shape_county_repository)
    mapped_county_repository.initialize()
    mapped_counties = mapped_county_repository.get_mapped_counties()
    for mapped_county in mapped_counties:
        county_name = mapped_county.get_dataset_county_name()
        for neighbour in mapped_county.get_neighbours():
            neighbour_county_name = neighbour
            try:
                neighbour_county = mapped_county_repository.get_mapped_county_by_canonic_name(neighbour)
                canonic_neighbour_county_name = neighbour_county.get_dataset_county_name()
                print(f"MATCH (a:Record), (b:Record) WHERE a.countyName = '{county_name}' "
                      f"AND b.countyName = '{canonic_neighbour_county_name}' "
                      f"CREATE (a)-[r:NEIGHBOUR_COUNTY]->(b) RETURN r")
            except AttributeError as error:
                print(f"county: {county_name}, neighbour: {neighbour_county_name}")


if __name__ == '__main__':

    __server_uri: str = "bolt://127.0.0.1:7687"
    __username: str = "neo4j"
    __password: str = "graphdb"

    path_to_shape_file = "tests/testfiles/de_county.shp"
    path_to_dataset_file = "tests/testfiles/january_2022_first_day.csv"
    csv_dataset_loader = CsvDatasetLoader(path_to_dataset_file)
    datapoint_repository = DatapointRepository(csv_dataset_loader)
    name_normalizer = CountyNameNormalizer()
    dataset_county_factory = DatasetCountyFactory(name_normalizer)
    shape_county_factory = ShapeCountyFactory(name_normalizer)
    shape_county_repository = ShapeCountyRepository(ShapefileLoader(path_to_shape_file, shape_county_factory))
    dataset_county_repository = DatasetCountyRepository(datapoint_repository, dataset_county_factory)
    county_mapper = CountyMapper(dataset_county_repository, shape_county_repository)

    # import_datasets()

    create_relations()

