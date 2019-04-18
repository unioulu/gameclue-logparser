import csv
import os
from MutationParser import MutationParser
from LogFileParser import LogFileParser


class LogFile(object):
    """LogFile is a class that represents a gameclue/spacegame log file.
       Takes path of the logfile and reads its data for easier access."""

    def __init__(self, file_path):
        super(LogFile, self).__init__()
        self.path = file_path
        self.file_name = self.__get_file_name(file_path)
        self.file_base_name = self.__get_file_base_name(file_path)
        self.file_extension = self.__get_file_extension(file_path)
        self.data = self._read_data(file_path)
        self.num_of_lines = self._calculate_num_of_lines(file_path)
        self.mutations = self._find_mutations()
        self.has_cues = self._has_cues(file_path)

    def _read_data(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            data = []
            for row in reader:
                data.append(row)
            return data

    def _calculate_num_of_lines(self, file_path):
        """ Calculate the number of lines """
        with open(file_path) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def __get_file_name(self, file_path):
        """ '/path/to/file.txt' -> 'file.txt' """
        return os.path.basename(file_path)

    def __get_file_base_name(self, file_path):
        """ '/path/to/file.txt' -> 'file' """
        return os.path.basename(os.path.splitext(file_path)[0])

    def __get_file_extension(self, file_path):
        """ '/path/to/file.txt' -> '.txt' """
        return os.path.basename(os.path.splitext(file_path)[1])

    def _find_mutations(self):
        """ Finds mutations from a file and return a list of Mutations """
        return MutationParser.parse(self)

    def _has_cues(self, file_path):
        """ Finds out if the LogFile has Cues. """
        return LogFileParser.hasCues(self, file_path)
