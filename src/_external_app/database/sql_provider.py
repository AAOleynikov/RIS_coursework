import os


class SQLProvider:
    def __init__(self, file_path):
        self.scripts = {}
        for file in os.listdir(file_path):
            self.scripts[file] = open(f'{file_path}/{file}').read()

    def get(self, file):
        return self.scripts[file]
