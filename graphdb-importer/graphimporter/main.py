from graphimporter.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.GraphImporter import GraphImporter
from graphimporter.Neo4jDatabaseConnection import Neo4jDatabaseConnection
from graphimporter.repositories.Neo4jRepository import Neo4jRepository

if __name__ == '__main__':
    __server_uri: str = "bolt://127.0.0.1:7687"
    __username: str = "neo4j"
    __password: str = "graphdb"

    __path_to_shape_file = "tests/testfiles/de_county.shp"
    __path_to_dataset_file = "tests/testfiles/january_2022_first_day.csv"

    neo4j_database_connection = Neo4jDatabaseConnection(__server_uri, __username, __password)
    datapoint_node_mapper = DatapointNodeMapper()
    neo4j_repository = Neo4jRepository(neo4j_database_connection, datapoint_node_mapper)
    graph_importer = GraphImporter(neo4j_repository, __path_to_dataset_file,
                                   __path_to_shape_file)
    graph_importer.import_datasets()
    graph_importer.create_relations()
