import json


def generate_preamble(file: str):
    with open(file, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
        document_option = ', '.join(data['document_option'])
        base = f'\\documentclass[{document_option}]{{{data["document_class"]}}}\n\n'
        if not data['preamble']:
            return base
        return base + data['preamble'] + '\n\n'


def generate_title(file: str):
    with open(file, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
        return f'\\helloworld{{{data["year"]}}}{{{data["school"]}}}{{{data["class"]}}}{{{data["subject"]}}}\n'


def generate_section(file: str, index: int, content: str):
    with open(file, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
        title = data['sections'][index - 1]
        section_head = f'\\section{{{title}}}\n'
        return section_head + '\\begin{cquestions}\n' + content + '\n\\end{cquestions}\n'


if __name__ == '__main__':
    print(generate_section("Test/config/104.json", 1, '\tabcabc'))
