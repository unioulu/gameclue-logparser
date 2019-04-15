import csv
import random


class CSVWriter(object):
    """
    CSVWriter is a class that is capable of writing given LogFile(s) to disk.
    """

    def __init__(self):
        super(CSVWriter, self).__init__()

    def write(self, LogFile, output_folder_path):
        print(output_folder_path)
        print(LogFile.path)
        outputti = f"{output_folder_path}{random.randint(1,1000)}"
        with open(outputti, 'w+', newline='') as out:
            writer = csv.writer(out, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(LogFile.data)
