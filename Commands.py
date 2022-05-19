import os
from PypOrganizer import Problem, ProblemOrganizer
from ConfigOrganizer import *


def __find_all_occurrence(base: str, name: str):
    """
    Finds all files with a certain name in a directory.
    :param base: the base directory
    :param name: the file name
    :return: All files in the base directory having the given name
    """
    matches = []
    for root, directories, files in os.walk(base):
        for file in files:
            if file == name:
                matches.append(os.path.join(root, file))
    return matches


def group_problems(base: str, name: str):
    problems = []
    for file in __find_all_occurrence(base, name):
        organizer = ProblemOrganizer(path=file)
        problems += organizer.group_problems()
    return problems


def sort_problems(problems: list[Problem]):
    problems_with_keys = sorted(problems, key=lambda p: p.get_number())
    sections = set(n for n in map(lambda p: p.get_section(), problems_with_keys))
    result = dict()
    for s in sections:
        result[s] = [p.get_content() for p in problems_with_keys if p.get_section() == s]
    return result


def generate_problems(base: str, name: str, config_path: str):
    problems = sort_problems(group_problems(base, name))
    output = [generate_preamble(config_path),
              BEGIN_DOCUMENT,
              generate_title(config_path)]
    for section in sorted(problems.keys()):
        section_problem = problems[section]
        output.append(generate_section(config_path, int(section)))
        output.append(BEGIN_QUESTION)
        for problem in section_problem:
            output.append(problem + '\n\n')
        output.append(END_QUESTION)
    output.append(END_DOCUMENT)

    return output


def organize_problems(base: str, name: str, dest: str, dest_name: str, config_path: str):
    problems = generate_problems(base, name, config_path)
    if not os.path.exists(dest):
        os.makedirs(dest)
    dest_file = os.path.join(dest, dest_name)
    with open(dest_file, 'w', encoding=ENCODING) as file:
        file.writelines(problems)


if __name__ == '__main__':
    organize_problems('Test', '104.tex', 'out/Test', '104.tex', 'Test/config/104.json')
