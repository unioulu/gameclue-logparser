import csv
import random


class CSVWriter(object):
    """
    CSVWriter is a class that is capable of writing given LogFile(s) to disk.
    """

    def __init__(self):
        super(CSVWriter, self).__init__()

    def write(self, LogFile, output_folder_path):
        output = f"{output_folder_path}{LogFile.file_base_name}{LogFile.file_extension}"
        with open(output, 'w+', newline='') as out:
            writer = csv.writer(out, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(LogFile.data)
            print(f"Write: {output}")

    def write_mutation(self, LogFile, output_folder_path):
        for mutation in LogFile.mutations:
            output = f"{output_folder_path}{LogFile.file_base_name}{mutation.name}"
            with open(output, 'w+', newline='') as out:
                writer = csv.writer(out, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writerows(mutation.data)
                print(f"Write: {output}")
