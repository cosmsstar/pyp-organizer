import os
from PypOrganizer import ProblemOrganizer
from functools import cmp_to_key


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
    def __compare_problem_keys(problem1, problem2):
        key1, key2 = problem1[0], problem2[0]
        if key1[0] != key2[0]:
            return key1[0] - key2[0]
        return key1[1] - key2[1]

    problems_with_keys = map(ProblemOrganizer.extract_keys, problems)
    return sorted(problems_with_keys, key=cmp_to_key(__compare_problem_keys))


def organize_problems(base: str, name: str, dest: str, dest_name: str):
    problems = sort_problems(group_problems(base, name))
    if not os.path.exists(dest):
        os.makedirs(dest)
    dest_file = os.path.join(dest, dest_name)
    with open(dest_file, 'w', encoding='utf-8-sig') as file:
        file.writelines(map(lambda pro: f'{pro[1]}\n\n', problems))


if __name__ == '__main__':
    organize_problems('Test', '104.tex', 'out/Test', '104.tex')
