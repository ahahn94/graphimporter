from graphimporter.GraphImporter import GraphImporter

if __name__ == '__main__':
    __server_uri: str = "bolt://127.0.0.1:7687"
    __username: str = "neo4j"
    __password: str = "graphdb"

    __path_to_shape_file = "tests/testfiles/de_county.shp"
    __path_to_dataset_file = "tests/testfiles/january_2022_first_day.csv"

    graph_importer = GraphImporter(server_uri=__server_uri, username=__username, password=__password,
                                   path_to_dataset_file=__path_to_dataset_file, path_to_shape_file=__path_to_shape_file)
    graph_importer.import_datasets()
    graph_importer.create_relations()
