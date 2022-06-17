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

    def get_county_type(self):
        return self._county_type

    def same_county(self, other_county: 'County') -> bool:
        names_match = self._name == other_county.get_name()
        canonic_names_match = self._canonic_name == other_county.get_canonic_name()
        types_match = self._county_type == other_county.get_county_type()
        return names_match and canonic_names_match and types_match
