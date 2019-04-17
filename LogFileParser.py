import csv

class LogFileParser(object):
    """docstring for LogFileParser."""

    def __init__(self):
        super(LogFileParser, self).__init__()

    def _read_data(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            data = []
            for row in reader:
                data.append(row)
            return data

    def hasCues(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            timestamp, HasCues = next(reader)
            if "HasCues" in HasCues:
                if "HasCues|True" in HasCues:
                    return True
                if "HasCues|False" in HasCues:
                    return False
            else:
                raise ValueError(f'{file_path} did not have HasCues on its 1st row.')
