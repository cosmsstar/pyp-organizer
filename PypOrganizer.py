from ConfigOrganizer import ENCODING


class Problem:
    """
    A class that represents a problem.
    """

    def __init__(self, problem: str):
        numbers = problem.split()[1].split('-')
        self.__key = tuple(map(lambda num: float(num), numbers))
        self.__problem = problem

    def __str__(self):
        return self.__problem.split('\n')[3].strip()[:15] + '...'

    def get_section(self):
        return self.__key[0]

    def get_number(self):
        return self.__key[1]

    def get_content(self):
        return self.__problem


class ContentExtractor:
    """
    A class that stores the content of a file as a list of strings.
    """

    def __init__(self, path: str):
        """
        Constructs a ContentExtractor according to the given file path.
        :param path: The path of the file.
        """
        self.path = path
        with open(path, 'r', encoding=ENCODING) as file:
            self.lines = file.readlines()

    def __str__(self):
        return f"ContentExtractor @ {self.path}"

    def print_content(self):
        for line in self.lines:
            print(line, end='')


class ProblemOrganizer:
    """
    A class that parses a tex file to problems.
    """

    def __init__(self, extractor: ContentExtractor = None, path: str = None):
        if not extractor and not path:
            raise Exception("Please provide a path or a ProblemExtractor!")

        if not extractor:
            self.extractor = ContentExtractor(path)
        else:
            self.extractor = extractor

    def __str__(self):
        return self.extractor.__str__()

    def __filter_content(self):
        """
        Filter out contents that are not part of the answers / questions, including the titles.
        :return: the filtered list of content.
        """
        return list(filter(lambda line: line.startswith('    ') or
                                        line.startswith('\t') or
                                        not line.strip(), self.extractor.lines))

    def group_problems(self):
        group = []
        contents = self.__filter_content()
        is_start = False
        current_problem = ''
        for line in contents:
            is_start = is_start or line.strip().startswith('%->')
            if not is_start:
                continue
            if line.strip().startswith('%->') and current_problem:
                group.append(current_problem.rstrip())
                current_problem = line
            else:
                current_problem += line

        if current_problem:
            group.append(current_problem.rstrip())

        return list(map(lambda p: Problem(p), group))
