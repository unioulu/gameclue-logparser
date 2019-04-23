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
        """
        All original log files should have ["0","HasCues|True"] on the
        first line. IF the cues have been disabled, it can be seen on the very
        second line of the file. The second line in that case should be:
            >>> ["{timestamp}", "HasCues|False"]

        This method is optimistic. Any later changes to cues (after lines
        0 and 1) are not taken into account.
        """
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            first_line = next(reader)  # First line
            second_line = next(reader)

            first_timestamp, first_event = first_line
            second_timestamp, second_event = second_line
            if "HasCues|True" in first_event:
                if "HasCues|False" in second_event:
                    return False
                else:
                    return True
            else:
                raise ValueError(f'{file_path} did not have HasCues on its 1st row.')
