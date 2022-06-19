class RawCounty:

    county_name: str
    type_name: str

    def __init__(self, county_name, type_name):
        self.county_name = county_name
        self.type_name = type_name

    def __eq__(self, other: 'RawCounty') -> bool:
        return self.county_name == other.county_name and self.type_name == other.type_name

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __str__(self) -> str:
        return self.type_name + " " + self.county_name
