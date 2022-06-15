from County import County


class CountyList:

    def __init__(self):
        self.__list = []

    def empty(self):
        return len(self.__list) == 0

    def append(self, county: County):
        self.__list.append(county)

    def get_county_for_canonic_name(self, canonic_name: str):
        for county in self.__list:
            if county.get_canonic_name() == canonic_name:
                return county
        raise NoSuchCountyException

    def get(self, index):
        if (index >= 0 and index < len(self.__list)):
            return self.__list.__getitem__(index)


class NoSuchCountyException(Exception):
    pass
