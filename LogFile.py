import csv
from Mutation import Mutation


class LogFile(object):
    """LogFile is a class that represents a gameclue/spacegame log file.
       Takes path of the logfile and reads its data for easier access."""

    def __init__(self, file_path):
        super(LogFile, self).__init__()
        self.path = file_path
        self.num_of_lines = self._calculate_num_of_lines(file_path)
        self.sanitized = self._is_timestamp_normalized(file_path)
        self.data = self._read_data(file_path)
        self.mutations = self._find_mutations(file_path)

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

    def _find_mutations(self, file_path):
        return [Mutation]
        """ Finds mutations from a file and return a list of Mutations """

    def _is_timestamp_normalized(self, file_path):
        """ Checks if the logfile is timestamp normalized """

    def getRowByTimestamp():
        """ Returns a full row of data by timestamp """
