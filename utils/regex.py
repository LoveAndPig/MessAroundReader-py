import re


class MyRegex:
    default_regex = r"^第?\s*\d+\s*(?:章\s*节?|节|话|話|\s+)"

    def __init__(self):
        self.__regexes = []
        self.load_regexes()

    def load_regexes(self):
        try:
            with open('regex.lsy', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if self.is_valid_regex(line.strip()):
                        self.__regexes.append(line.strip())
                if len(self.__regexes) == 0:
                    self.__regexes.append(self.default_regex)
        except FileNotFoundError:
            self.__regexes.append(self.default_regex)

    def save_regexes(self):
        try:
            with open('regex.lsy', 'w', encoding='utf-8') as f:
                for regex in self.__regexes:
                    f.write(regex + '\n')
                    f.flush()
        except FileNotFoundError:
            pass

    def is_string_match_regex(self, string) -> bool:
        for regex in self.__regexes:
            if re.match(regex, string):
                return True
        return False

    def add_regex(self, regex) -> bool:
        if self.is_valid_regex(regex):
            self.__regexes.append(regex)
            return True
        else:
            return False

    @staticmethod
    def is_valid_regex(regex) -> bool:
        try:
            re.compile(regex)
            return True
        except re.error:
            return False


regex_util = MyRegex()
