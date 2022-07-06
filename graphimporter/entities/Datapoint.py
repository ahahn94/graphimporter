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

    def __str__(self):
        return f"Datapoint {{ state: {self.__state}, county: {self.__county}, age_group: {self.__age_group}, " \
               f"gender: {self.__gender}, date: {self.__date}, cases: {self.__cases}, deaths: {self.__deaths}, " \
               f"recovered: {self.__recovered} }}"

    def identifiers_string(self):
        return f"county: {self.__county}, age_group: {self.__age_group}, gender: {self.__gender}, date: {self.__date}"

    def __eq__(self, other):
        age_match = self.__age_group == other.get_age_group()
        cases_match = self.__cases == other.get_cases()
        county_match = self.__county == other.get_county()
        date_match = self.__date == other.get_date()
        deaths_match = self.__deaths == other.get_deaths()
        gender_match = self.__gender == other.get_gender()
        recovered_match = self.__recovered == other.get_recovered()
        state_match = self.__state == other.get_state()
        return age_match and cases_match and county_match and date_match and deaths_match and gender_match \
            and recovered_match and state_match
