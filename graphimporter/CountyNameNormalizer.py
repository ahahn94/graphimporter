import re


class CountyNameNormalizer:

    def __init__(self) -> None:
        super().__init__()

    def normalize(self, county_name: str):
        county_name = self.__replace_umlaute_lower_case(county_name)
        county_name = self.__replace_umlaute_upper_case(county_name)
        county_name = self.__handle_special_cases(county_name)
        county_name = self.__replace_prepositions(county_name)
        county_name = self.__replace_text_in_brackets(county_name)
        county_name = self.__strip_whitespaces(county_name)
        return county_name

    @staticmethod
    def __replace_umlaute_lower_case(county_name: str):
        return county_name.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")

    @staticmethod
    def __replace_umlaute_upper_case(county_name: str):
        return county_name.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE").replace("ẞ", "SS")

    @staticmethod
    def __handle_special_cases(county_name: str):
        county_name = county_name.replace("Sankt", "St.")
        county_name = county_name.replace("Eifelkreis ", "")
        county_name = county_name.replace("Regionalverband ", "")
        county_name = county_name.replace("Stadtverband ", "")
        county_name = county_name.replace("Ludwigshafen am Rhein", "Ludwigshafen")
        county_name = county_name.replace("Offenbach am Main", "Offenbach")
        county_name = county_name.replace("LK Region", "Region")
        county_name = county_name.replace("LK Staedteregion", "StaedteRegion")
        return county_name

    @staticmethod
    def __replace_prepositions(county_name: str):
        county_name = county_name.replace("am ", "a.").replace("a. ", "a.")
        county_name = county_name.replace("an der ", "a.d.").replace("a.d. ", "a.d.")
        county_name = county_name.replace("im ", "i.").replace("i. ", "i.")
        county_name = county_name.replace("in der ", "i.d.").replace("i.d. ", "i.d.")
        return county_name

    @staticmethod
    def __replace_text_in_brackets(county_name: str):
        return re.sub(r" \([a-zA-Zäöüß]*\)", "", county_name)

    @staticmethod
    def __strip_whitespaces(county_name: str):
        return county_name.strip()
