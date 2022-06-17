from graphimporter.entities.CountyType import CountyType


class County:

    _canonic_name: str
    _name: str
    _county_type: CountyType

    def __init__(self, name: str, county_type: CountyType):
        self._name = name
        self._county_type = county_type
        self.determine_canonic_name()

    def get_canonic_name(self):
        return self._canonic_name

    def determine_canonic_name(self):
        pass
