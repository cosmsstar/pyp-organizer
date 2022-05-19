import json


BEGIN_DOCUMENT = '\\begin{document}\n\n'
END_DOCUMENT = '\\end{document}\n'
BEGIN_QUESTION = '\\begin{cquestions}\n\n'
END_QUESTION = '\\end{cquestions}\n\n'


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
        return f'\\helloworld{{{data["year"]}}}{{{data["school"]}}}{{{data["class"]}}}{{{data["subject"]}}}\n\n'


def generate_section(file: str, index: int):
    with open(file, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
        title = data['sections'][index - 1]
        explanation = data['section_explanations'][index - 1]
        if not explanation:
            return f'\\section{{{title}}}\n\n'
        return f'\\section{{{title}}}\n\n{explanation}\n\n'


if __name__ == '__main__':
    print(generate_section("Test/config/104.json", 1))
