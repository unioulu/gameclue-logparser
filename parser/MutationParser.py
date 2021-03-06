import sanitizer as s
import csv
import statistics
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

            mutation = Mutation(mutationName, mutation_data, mutationOrder)

            mutation_data.append([MutationParser.findLastTimeStampOfMutation(mutation), "LastRow"])
            Mutations.append(mutation)
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

    def getNumberOfOccurences(Mutation, occurence):
        amnt = 0
        for line in Mutation.data:
            timestamp, event = line
            if(event == occurence):
                amnt += 1
        return amnt

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
        return None

    def findLastTimeStamp(Mutation, key):
        last = None
        for line in Mutation.data:
            timestamp, event = line
            if key in event:
                last = timestamp
        return last

    def findLastTimeStampOfMutation(Mutation):
        timestamp, event=Mutation.data[len(Mutation.data)-1]
        return timestamp

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
            hold_timestamps.append(None)
        return hold_timestamps

    def findOccurencesThatStartWith(Mutation, occurence):
        timestamps = []
        for line in Mutation.data:
            timestamp, event = line
            if event.startswith(occurence):
                timestamps.append(float(timestamp))
        return timestamps

    def findOccurencesThatStartWithAny(Mutation, occurenceList):
        timestamps = []
        for line in Mutation.data:
            timestamp, event = line
            for occurence in occurenceList:
                if event.startswith(occurence):
                    timestamps.append(float(timestamp))
        return timestamps

    def getInputsPerMinute(Mutation, start = None, end = None):
        amnt = 0
        firstOccurence = 0
        lastOccurence = 0
        for line in Mutation.data:
            timestamp, event = line
            if (amnt == 1):
                firstOccurence = float(timestamp)
            if (start == None or end == None):
                if (event.startswith("KeyDown")):
                    amnt += 1
                    lastOccurence = float(timestamp)
            else:
                if (event.startswith(start) and event.endswith(end)):
                    amnt += 1
                    lastOccurence = float(timestamp)
        if (amnt == 0):
            print("No occurences")
            return None
        elif (lastOccurence == firstOccurence):
            print("Occurence happened only once")
            return None
        return round(amnt / ((lastOccurence - firstOccurence)/60), 3)

    def calculateDiffs(Mutation, occurence):
        diffs = []
        lastTime = 0
        times = MutationParser.findOccurencesThatStartWith(
            Mutation, occurence)
        for c, time in enumerate(times):
            if (c > 0):
                diffs.append(time - lastTime)
            else:
                diffs.append(time)
            lastTime = time
        if (len(diffs) > 0):
            longest = max(diffs)
            shortest = min(diffs)
            average = statistics.median(diffs)
        else:
            return None, None, None
        return round(longest, 3), round(shortest, 3), round(average, 3)

    def calculateRanges(Mutation, startPointList, endPointList):
        diffs = []
        starts = MutationParser.findOccurencesThatStartWithAny(
            Mutation, startPointList)
        ends = MutationParser.findOccurencesThatStartWithAny(Mutation, endPointList)
        for c, time in enumerate(starts):
            diffs.append(ends[c] - time)
        if (len(diffs) > 0):
            longest = max(diffs)
            shortest = min(diffs)
            average = statistics.median(diffs)
        else:
            return None, None, None
        return round(longest, 3), round(shortest, 3), round(average, 3)
