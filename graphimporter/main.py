from os import path

from graphimporter.mappers.DatapointNodeMapper import DatapointNodeMapper
from graphimporter.GraphImporter import GraphImporter
from graphimporter.Neo4jDatabaseConnection import Neo4jDatabaseConnection
from graphimporter.repositories.Neo4jRepository import Neo4jRepository


def main():
    # Replace these by your Neo4j server connection parameters.
    __server_uri: str = "bolt://127.0.0.1:7687"
    __username: str = "neo4j"
    __password: str = "graphdb"

    # Replace these with the paths to your county shape and case numbers files.
    __path_to_shape_file = path.dirname(__file__) + "/tests/testfiles/de_county.shp"
    __path_to_dataset_file = path.dirname(__file__) + "/tests/testfiles/january_2022.csv"

    # Assemble components.
    neo4j_database_connection = Neo4jDatabaseConnection(__server_uri, __username, __password)
    datapoint_node_mapper = DatapointNodeMapper()
    neo4j_repository = Neo4jRepository(neo4j_database_connection, datapoint_node_mapper)
    graph_importer = GraphImporter(neo4j_repository, __path_to_dataset_file,
                                   __path_to_shape_file)
    # Import datasets and relationships into Neo4j.
    graph_importer.import_datasets_and_relationships()


if __name__ == '__main__':
    main()
