import sanitizer as s
import csv
from itertools import islice
from Mutation import Mutation

class MutationParser(object):
    """docstring for MutationParser."""

    def __init__(self):
        super(MutationParser, self).__init__()

    def parse(LogFile):
        """ Returns a list of Mutation objects """
        logfile = LogFile.path
        mutationRanges = MutationParser.findMutationRanges(logfile)
        mutation_list = []

        for mutation in mutationRanges:
            mutation_data = []
            mutationStart = mutationRanges.get(mutation)[0]
            mutationEnd = mutationRanges.get(mutation)[1]
            mutationName = mutation.split("Scene")[0]
            # print(f"Mutation name: {mutationName}")
            # print(f"Mutation start line: {mutationStart}")
            # print(f"Mutation end line  : {mutationEnd}")

            with open(f'{logfile}') as f:
                reader = csv.reader(f, delimiter=';', quotechar='"')

                for row in islice(reader, mutationStart, mutationEnd):
                    mutation_data.append(row)

            # mutation_list.append(mutation_data)
            mutation_list.append(Mutation(mutationName, mutation_data))
        return mutation_list

    def findMutationRanges(logfile):

        mutationRanges = {
          "BaseGameScene":     [],  # BaseGame doesn't produce "ChangedScene" event
          "ShootGameScene":    [],
          "PointGameScene":    [],
          "MovementGameScene": [],
          "InputGameScene":    []
        }

        # Find all scene changes, we can find line ranges by doing this.
        mutationChangeLines = MutationParser.getAllOccurencesLineNumbers(logfile, "ChangedScene")

        # BaseGame mutation starts on first occurence of GameStarted
        # (ChangeScene|BaseGame is not written to logs)
        gameStartedLine = s.getFirstOccurenceLineNumber(logfile, "GameStarted")
        mutationChangeLines.insert(0, gameStartedLine)

        # Last mutation ends to the very last line of the file
        mutationChangeLines.append(MutationParser.getLastLineNumber(logfile))

        # Find start and end line numbers for each mutation
        shootGameSceneLineStart = s.getFirstOccurenceLineNumber(
            logfile, "ChangedScene|ShootGameScene")
        shootGameSceneLineEnd = MutationParser.getNextMutationLineNumber(
            logfile, shootGameSceneLineStart)

        pointGameSceneLineStart = s.getFirstOccurenceLineNumber(
            logfile, "ChangedScene|PointGameScene")
        pointGameSceneLineEnd = MutationParser.getNextMutationLineNumber(
            logfile, pointGameSceneLineStart)

        movementGameSceneLineStart = s.getFirstOccurenceLineNumber(
            logfile, "ChangedScene|MovementGameScene")
        movementGameSceneLineEnd = MutationParser.getNextMutationLineNumber(
            logfile, movementGameSceneLineStart)

        inputGameSceneLineStart = s.getFirstOccurenceLineNumber(
            logfile, "ChangedScene|InputGameScene")
        inputGameSceneLineEnd = MutationParser.getNextMutationLineNumber(
            logfile, inputGameSceneLineStart)

        # Store mutation line number ranges to a dictionary
        mutationRanges["BaseGameScene"] = [
            mutationChangeLines[0], mutationChangeLines[1]]
        mutationRanges["ShootGameScene"] = [
            shootGameSceneLineStart, shootGameSceneLineEnd]
        mutationRanges["PointGameScene"] = [
            pointGameSceneLineStart, pointGameSceneLineEnd]
        mutationRanges["MovementGameScene"] = [
            movementGameSceneLineStart, movementGameSceneLineEnd]
        mutationRanges["InputGameScene"] = [
            inputGameSceneLineStart, inputGameSceneLineEnd]

        return mutationRanges


    def splitToFiles(mutations, args):
        with open(logfile) as f:
            outputfile = open("./output/tiedosto.txt", "w")
            for i, line in enumerate(f):
                if i >= shootGameSceneLineStart and i <= shootGameSceneLineEnd:
                    outputfile.write(line)


    def getLastLineNumber(logfile):
        return sum(1 for line in open(logfile))


    def getMutationRange(logfile, mutationName):
        startLine = s.getFirstOccurenceLineNumber(logfile, mutationName)


    def getNextMutationLineNumber(logfile, startLineNumber):
        with open(logfile, 'r') as f:
            for (i, line) in enumerate(f):
                if startLineNumber < i:
                    if "ChangedScene" in line:
                        return i
        return MutationParser.getLastLineNumber(logfile)  # Return last line number if not found


    def getAllOccurencesLineNumbers(logfile, logEntry):
        res = []
        with open(logfile, 'r') as f:
            for (i, line) in enumerate(f):
                if logEntry in line:
                    res.append(i)
            return res
        return -1

    def findFirstTimestamp(Mutation, key):
        for line in Mutation.data:
            timestamp, event = line
            if key in event:
                return timestamp
        return 'null'
