import csv
import random
from Counter import Counter


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
                writer.writerow(['timestamp','event'])
                writer.writerows(mutation.data)
                print(f"Write: {output}")

    def write_mutation_report(self, LogFiles, output_folder_path):

        output = f"{output_folder_path}MutationReport.csv"
        header = ['user', 'mutation', 'hasCues', 'mutationPlayedInOrder',
                  'playerDeaths', 'normalShotsFired', 'chargeShotsFired', 'timeFirstPositiveCollected',
                  'timeLastPositiveCollected', 'totalPositivesCollected', 'totalNegativesCollected']

        with open(output, 'w+', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=header, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for logfile in LogFiles:
                for mutation in logfile.mutations:

                    normalShotsFired = Counter.countKeys(mutation, "PlayerFiredNormalShot")
                    playerDeaths = Counter.countKeys(mutation, "GameEnded|PlayerDied")

                    writer.writerow({'user': logfile.file_base_name,
                                     'mutation': mutation.name,
                                     'hasCues': logfile.has_cues,
                                     'mutationPlayedInOrder': None,
                                     'playerDeaths': playerDeaths,
                                     'normalShotsFired': normalShotsFired,
                                     'chargeShotsFired': None,
                                     'timeFirstPositiveCollected': None,
                                     'timeLastPositiveCollected': None,
                                     'totalPositivesCollected': None,
                                     'totalNegativesCollected': None,
                                    })

        print(f'Write: {output}')

# writer = csv.DictWriter(open("ChartData.csv", 'a' ), headers)
