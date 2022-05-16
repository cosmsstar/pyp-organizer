class ProblemExtractor:
    """
    A class that stores the content of a file as a list of strings.
    """

    def __init__(self, path: str):
        """
        Constructs a ProblemExtractor according to the given file path.
        :param path: The path of the file.
        """
        self.path = path
        with open(path, 'r', encoding='UTF-8') as file:
            self.lines = file.readlines()

    def __str__(self):
        return self.path

    def print_content(self):
        print_content(self.lines)


def filter_content(extractor: ProblemExtractor):
    """
    Filter out contents that are not part of the answers / questions, including the titles.
    :param extractor: the ProblemExtractor we will deal with.
    :return: the filtered list of content.
    """
    return list(filter(lambda line: line.startswith('    ') or not line.strip(),
                       extractor.lines))


def print_content(contents):
    for line in contents:
        print(line, end='')


def group_problems(extractor: ProblemExtractor):
    group = []
    contents = filter_content(extractor)
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

    return group


def extract_keys(problem: str):
    """
    Extract the problem number as a key.
    :param problem: The problem to be processed.
    :return: the number of the problem.
    """
    numbers = problem.split()[1].split('-')
    return tuple(map(lambda num: int(num), numbers))
