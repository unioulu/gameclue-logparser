import csv
from util.Counter import Counter
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

        filename = "MutationReport.csv"
        output = f"{output_folder_path}{filename}"
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
                playerTimeAlive = 0
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

                    totalPositivesSpawned = Counter.countKeys(
                        mutation, "PickUpSpawned|Coin(Clone)")
                    totalNegativesSpawned = Counter.countKeys(
                        mutation, "PickUpSpawned|Coin_Negative(Clone)")
                    playerShortestTimeAlive = None
                    playerAverageTimeAlive = None

                    diffs = []
                    lastTime = 0
                    times = MutationParser.findOccurencesThatStartWith(
                        mutation, "PlayerDied")
                    for c, time in enumerate(times):
                        if (c > 0):
                            diffs.append(time - lastTime)
                        else:
                            diffs.append(time)
                        lastTime = time

                    if (len(diffs) > 0):
                        playerLongestTimeAlive = max(diffs)
                    else:
                        playerLongestTimeAlive = None

                    shotsPerMinute = MutationParser.getInputsPerMinute(
                        mutation, "KeyDown|Space")
                    inputsPerMinute = MutationParser.getInputsPerMinute(mutation)
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
                    timeLastPositiveCollected = MutationParser.findLastTimeStamp(
                        mutation, "PlayerCollidesWithPickUp|Coin(Clone)")
                    totalPositivesCollected = Counter.countKeys(mutation, "PlayerCollidesWithPickUp|Coin(Clone)")
                    timeLastNegativeCollected = MutationParser.findLastTimeStamp(
                        mutation, "PlayerCollidesWithPickUp|Coin_Negative(Clone)")
                    totalNegativesCollected = Counter.countKeys(mutation, "PlayerCollidesWithPickUp|Coin_Negative(Clone)")

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
                                     'totalPositivesSpawned': totalPositivesSpawned,
                                     'totalNegativesSpawned': totalNegativesSpawned,
                                     'playerShortestTimeAlive': playerShortestTimeAlive,
                                     'playerLongestTimeAlive': playerLongestTimeAlive,
                                     'playerAverageTimeAlive': playerAverageTimeAlive,
                                     'shotsPerMinute': shotsPerMinute,
                                     'inputsPerMinute': inputsPerMinute,
                                     'timeFirstInputKeyPressedLEFT': timeFirstInputKeyPressedLEFT,
                                     'timeFirstInputKeyPressedRIGHT': timeFirstInputKeyPressedRIGHT,
                                     'timeFirstInputKeyPressedUP': timeFirstInputKeyPressedUP,
                                     'timeFirstInputKeyPressedDOWN': timeFirstInputKeyPressedDOWN,
                                     'timeFirstInputKeyPressedSPACE': timeFirstInputKeyPressedSPACE,
                                     'inputKeySPACEWasPressedForOneSecond': inputKeySPACEWasPressedForOneSecond
                                     })

        print(f'Write: {output}')

# writer = csv.DictWriter(open("ChartData.csv", 'a' ), headers)
