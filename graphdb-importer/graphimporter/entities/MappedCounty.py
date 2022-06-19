from graphimporter.entities.County import County
from graphimporter.entities.DatasetCounty import DatasetCounty
from graphimporter.entities.ShapeCounty import ShapeCounty


class MappedCounty(County):

    __neighbours: list[str]

    def __init__(self, dataset_county: DatasetCounty, shape_county: ShapeCounty):
        super().__init__(dataset_county.get_name(), dataset_county.get_county_type(), dataset_county.get_canonic_name())
        self.__neighbours = shape_county.get_neighbours()
