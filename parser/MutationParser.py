import sanitizer as s
import csv
from itertools import islice
from Mutation import Mutation
import operator


class MutationParser(object):
    """docstring for MutationParser."""

    def __init__(self):
        super(MutationParser, self).__init__()

    def parse(LogFile):
        """ Returns a list of Mutation objects """
        mutationRanges = MutationParser.findMutationRanges(LogFile.path)
        sortedMutationTuples = sorted(mutationRanges.items(), key=operator.itemgetter(1))

        Mutations = []

        for i, mutation in enumerate(sortedMutationTuples):
            mutation_data = []

            mutationName = mutation[0].split("Scene")[0]
            mutationStart = mutation[1][0]
            mutationEnd = mutation[1][1]
            mutationOrder = i

            with open(LogFile.path) as f:
                reader = csv.reader(f, delimiter=';', quotechar='"')
                for row in islice(reader, mutationStart, mutationEnd):
                    mutation_data.append(row)

            Mutations.append(Mutation(mutationName, mutation_data, mutationOrder))
        return Mutations

    def findMutationRanges(logfile):

        # Note BaseGame doesn't produce "ChangedScene" event.
        mutationRanges = {
            "BaseGameScene": [],
            "ShootGameScene": [],
            "PointGameScene": [],
            "MovementGameScene": [],
            "InputGameScene": []
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
        shootGameSceneLineStart = s.getFirstOccurenceLineNumber(logfile, "ChangedScene|ShootGameScene")
        shootGameSceneLineEnd = MutationParser.getNextMutationLineNumber(logfile, shootGameSceneLineStart)

        pointGameSceneLineStart = s.getFirstOccurenceLineNumber(logfile, "ChangedScene|PointGameScene")
        pointGameSceneLineEnd = MutationParser.getNextMutationLineNumber(logfile, pointGameSceneLineStart)

        movementGameSceneLineStart = s.getFirstOccurenceLineNumber(logfile, "ChangedScene|MovementGameScene")
        movementGameSceneLineEnd = MutationParser.getNextMutationLineNumber(logfile, movementGameSceneLineStart)

        inputGameSceneLineStart = s.getFirstOccurenceLineNumber(logfile, "ChangedScene|InputGameScene")
        inputGameSceneLineEnd = MutationParser.getNextMutationLineNumber(logfile, inputGameSceneLineStart)

        # Store mutation line number ranges to a dictionary
        mutationRanges["BaseGameScene"] = [mutationChangeLines[0], mutationChangeLines[1]]
        mutationRanges["ShootGameScene"] = [shootGameSceneLineStart, shootGameSceneLineEnd]
        mutationRanges["PointGameScene"] = [pointGameSceneLineStart, pointGameSceneLineEnd]
        mutationRanges["MovementGameScene"] = [movementGameSceneLineStart, movementGameSceneLineEnd]
        mutationRanges["InputGameScene"] = [inputGameSceneLineStart, inputGameSceneLineEnd]

        return mutationRanges

    def getLastLineNumber(logfile):
        return sum(1 for line in open(logfile))

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

    def findLastTimeStamp(Mutation, key):
        last = 'null'
        for line in Mutation.data:
            timestamp, event = line
            if key in event:
                last = timestamp
        return last

    def calculateInputKeyIsHeldDownTime(Mutation, key, min_time_held_ms):
        """ Returns a list of timestamps when "min_time_held_ms" long hold have been initiated. """
        key_down = "KeyDown|" + key
        key_up = "KeyUp|" + key

        hold_timestamps = []

        for line in Mutation.data:
            timestamp, event = line
            if key_down in event:
                key_down_timestamp = timestamp
            if key_up in event:
                key_up_timestamp = timestamp
                time_held = float(key_up_timestamp.replace(',', '.')) - float(key_down_timestamp.replace(',', '.'))
                if (time_held > min_time_held_ms):
                    hold_timestamps.append(key_down_timestamp)

        if not hold_timestamps:
            hold_timestamps.append('null')
        return hold_timestamps
