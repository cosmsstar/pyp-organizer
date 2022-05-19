import os
from PypOrganizer import ProblemOrganizer
import ConfigOrganizer


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


def sort_problems(problems):
    problems_with_keys = sorted(map(ProblemOrganizer.extract_keys, problems), key=lambda p: p[0][1])
    sections = set(n for n in map(lambda p : p[0][0], problems_with_keys))
    result = dict()
    for s in sections:
        result[s] = [p[1] for p in problems_with_keys if p[0][0] == s]
    return result


def generate_problems(base: str, name: str, config_path: str):
    problems = sort_problems(group_problems(base, name))
    output = [ConfigOrganizer.generate_preamble(config_path),
              ConfigOrganizer.BEGIN_DOCUMENT,
              ConfigOrganizer.generate_title(config_path)]
    for section in sorted(problems.keys()):
        section_problem = problems[section]
        output.append(ConfigOrganizer.BEGIN_QUESTION)
        for problem in section_problem:
            output.append(problem + '\n\n')
        output.append(ConfigOrganizer.END_QUESTION)
    output.append(ConfigOrganizer.END_DOCUMENT)

    return output


def organize_problems(base: str, name: str, dest: str, dest_name: str, config_path: str):
    problems = generate_problems(base, name, config_path)
    if not os.path.exists(dest):
        os.makedirs(dest)
    dest_file = os.path.join(dest, dest_name)
    with open(dest_file, 'w', encoding='utf-8-sig') as file:
        file.writelines(problems)


if __name__ == '__main__':
    organize_problems('Test', '104.tex', 'out/Test', '104.tex', 'Test/config/104.json')
