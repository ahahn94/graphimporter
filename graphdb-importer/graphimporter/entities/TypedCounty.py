from graphimporter.entities.CountyType import CountyType


class TypedCounty:

    _canonic_name: str
    _county_type: CountyType

    def __init__(self, county_type: CountyType, canonic_name: str):
        self._county_type = county_type
        self._canonic_name = canonic_name

    def get_canonic_name(self):
        return self._canonic_name

    def get_county_type(self):
        return self._county_type

    def same_county(self, other_county: 'TypedCounty') -> bool:
        canonic_names_match = self._canonic_name == other_county.get_canonic_name()
        types_match = self._county_type == other_county.get_county_type()
        return canonic_names_match and types_match
