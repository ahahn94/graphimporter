class Datapoint:
    __age_group: str
    __cases: int
    __county: str
    __date: str
    __deaths: int
    __gender: str
    __recovered: int
    __state: str

    def __init__(self, state: str, county: str, age_group: str, gender: str, date: str, cases: int, deaths: int,
                 recovered: int):
        self.__state = state
        self.__county = county
        self.__age_group = age_group
        self.__gender = gender
        self.__date = date
        self.__cases = cases
        self.__deaths = deaths
        self.__recovered = recovered

    def get_age_group(self):
        return self.__age_group

    def get_cases(self):
        return self.__cases

    def get_county(self):
        return self.__county

    def get_deaths(self):
        return self.__deaths

    def get_date(self):
        return self.__date

    def get_gender(self):
        return self.__gender

    def get_recovered(self):
        return self.__recovered

    def get_state(self):
        return self.__state
