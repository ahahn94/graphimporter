class County:

    _canonic_name: str
    _name: str
    _county_type: str

    def __init__(self, name: str, type: str):
        self._name = name
        self._county_type = type
        self.determine_canonic_name()

    def get_canonic_name(self):
        return self._canonic_name

    def determine_canonic_name(self):
        pass
