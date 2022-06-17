from graphimporter.entities.County import County


class DatasetCounty(County):

    def __init__(self, name: str, type: str):
        super().__init__(name, type)

    def determine_canonic_name(self):
        self._canonic_name = self._name
