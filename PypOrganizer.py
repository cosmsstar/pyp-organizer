import click

class FileExtractor:
    """
    A class that stores the content of a file as a list of strings.
    """
    def __init__(self, path: str):
        """
        Constructs a FileExtractor according to the given file path.
        :param path: The path of the file.
        """
        self.path = path
        with open(path, 'r') as file:
            self.lines = file.readlines()

    def __str__(self):
        return self.path

