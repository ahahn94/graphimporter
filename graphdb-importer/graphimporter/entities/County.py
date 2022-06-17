from graphimporter.entities.CountyType import CountyType


class County:

    _canonic_name: str
    _name: str
    _county_type: CountyType

    def __init__(self, name: str, county_type: CountyType, canonic_name: str):
        self._name = name
        self._county_type = county_type
        self._canonic_name = canonic_name

    def get_name(self):
        return self._name

    def get_canonic_name(self):
        return self._canonic_name
