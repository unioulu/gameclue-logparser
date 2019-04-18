import csv
from Counter import Counter
from MutationParser import MutationParser


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
                writer.writerow(['timestamp', 'event'])
                writer.writerows(mutation.data)
                print(f"Write: {output}")

    def write_mutation_report(self, LogFiles, output_folder_path):

        output = f"{output_folder_path}MutationReport.csv"
        header = ['user',
                  'mutation',
                  'hasCues',
                  'mutationPlayedInOrder',
                  'playerDeaths',
                  'normalShotsFired',
                  'chargeShotsFired',
                  'timeFirstPositiveCollected',
                  'timeLastPositiveCollected',
                  'totalPositivesCollected',
                  'timeFirstNegativeCollected',
                  'timeLastNegativeCollected',
                  'totalNegativesCollected',
                  'timeFirstNormalShotFired',
                  'totalPositivesSpawned',
                  'totalNegativesSpawned',
                  'playerShortestTimeAlive',
                  'playerAverageTimeAlive',
                  'playerLongestTimeAlive',
                  'actionsPerMinute',
                  'shotsPerMinute',
                  'inputsPerMinute',
                  'timeFirstInputKeyPressedLEFT',
                  'timeFirstInputKeyPressedRIGHT',
                  'timeFirstInputKeyPressedUP',
                  'timeFirstInputKeyPressedDOWN',
                  'timeFirstInputKeyPressedSPACE',
                  'inputKeySPACEWasPressedForOneSecond']

        with open(output, 'w+', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=header, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for logfile in LogFiles:
                for mutation in logfile.mutations:

                    playerDeaths = Counter.countKeys(
                        mutation, "GameEnded|PlayerDied")
                    normalShotsFired = Counter.countKeys(
                        mutation, "PlayerFiredNormalShot")

                    chargeShotsFired = MutationParser.findFirstTimestamp(
                        mutation, "PlayerFiredChargedShot")

                    timeFirstPositiveCollected = MutationParser.findFirstTimestamp(
                        mutation, "PlayerCollidesWithPickUp|Coin(Clone)")
                    timeFirstNegativeCollected = MutationParser.findFirstTimestamp(
                        mutation, "PlayerCollidesWithPickUp|Coin_Negative(Clone)")

                    timeFirstNormalShotFired = MutationParser.findFirstTimestamp(
                        mutation, "PlayerFiredNormalShot")

                    timeFirstInputKeyPressedLEFT = MutationParser.findFirstTimestamp(
                        mutation, "KeyDown|LeftArrow")
                    timeFirstInputKeyPressedRIGHT = MutationParser.findFirstTimestamp(
                        mutation, "KeyDown|RightArrow")
                    timeFirstInputKeyPressedUP = MutationParser.findFirstTimestamp(
                        mutation, "KeyDown|UpArrow")
                    timeFirstInputKeyPressedDOWN = MutationParser.findFirstTimestamp(
                        mutation, "KeyDown|DownArrow")
                    timeFirstInputKeyPressedSPACE = MutationParser.findFirstTimestamp(
                        mutation, "KeyDown|Space")

                    inputKeySPACEWasPressedForOneSecond = MutationParser.calculateInputKeyIsHeldDownTime(
                        mutation, "Space", 1)[0]
                    timeLastPositiveCollected = None
                    totalPositivesCollected = None
                    timeLastNegativeCollected = None
                    totalNegativesCollected = None

                    writer.writerow({'user': logfile.file_base_name,
                                     'mutation': mutation.name,
                                     'hasCues': logfile.has_cues,
                                     'mutationPlayedInOrder': mutation.played_in_order,
                                     'playerDeaths': playerDeaths,
                                     'normalShotsFired': normalShotsFired,
                                     'chargeShotsFired': chargeShotsFired,
                                     'timeFirstPositiveCollected': timeFirstPositiveCollected,
                                     'timeLastPositiveCollected': timeLastPositiveCollected,
                                     'totalPositivesCollected': totalPositivesCollected,
                                     'timeFirstNegativeCollected': timeFirstNegativeCollected,
                                     'timeLastNegativeCollected': timeLastNegativeCollected,
                                     'totalNegativesCollected': totalNegativesCollected,
                                     'timeFirstNormalShotFired': timeFirstNormalShotFired,
                                     'timeFirstInputKeyPressedLEFT': timeFirstInputKeyPressedLEFT,
                                     'timeFirstInputKeyPressedRIGHT': timeFirstInputKeyPressedRIGHT,
                                     'timeFirstInputKeyPressedUP': timeFirstInputKeyPressedUP,
                                     'timeFirstInputKeyPressedDOWN': timeFirstInputKeyPressedDOWN,
                                     'timeFirstInputKeyPressedSPACE': timeFirstInputKeyPressedSPACE,
                                     'inputKeySPACEWasPressedForOneSecond': inputKeySPACEWasPressedForOneSecond
                                     })

        print(f'Write: {output}')

# writer = csv.DictWriter(open("ChartData.csv", 'a' ), headers)
