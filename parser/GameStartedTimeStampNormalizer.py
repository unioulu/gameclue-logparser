from LogFileSanitizer import LogFileSanitizer


class GameStartedTimeStampNormalizer(LogFileSanitizer):
    """
    GameStartedTimeStampNormalizer is a type of sanitizer, that "resets" the
    LogFile timestamps to start from 0.

    This sanitation is required due the fact that the gameclue-spacegame first
    log entry (row) is logged right away when the game is launched. The time,
    when the game actually starts is at the first occurence of "GameStarted"
    key.
    """

    def __init__(self):
        super(GameStartedTimeStampNormalizer, self).__init__()

    def sanitize(self, LogFile):
        """ Returns sanitized, timestamp normalized LogFile """
        gameStartedRow = self.getFirstOccurenceLineNumber(
            LogFile, "GameStarted")
        if gameStartedRow != -1:
            timestamp_delta, other = LogFile.data[gameStartedRow]

            for i, (timestamp, events) in enumerate(LogFile.data):
                # print(LogFile.data[i][0])
                LogFile.data[i][0] = '%g' % (float(timestamp.replace(
                    ',', '.')) - float(timestamp_delta.replace(',', '.')))
        else:
            print(f"Could not find the first occurence of {logEntry} in {LogFile.path}")

        return LogFile

    def getFirstOccurenceLineNumber(self, LogFile, logEntry):
        with open(LogFile.path, 'r') as f:
            for (i, line) in enumerate(f):
                if logEntry in line:
                    return i
        return -1
