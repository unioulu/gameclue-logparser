from LogFileSanitizer import LogFileSanitizer


class MutationTimeStampNormalizer(LogFileSanitizer):
    """MutationTimeStampNormalizer normalizes LogFile mutations timestamps todo
        to start from 0.

        Simply takes the first line, assing the timestamps of it to zero and
        saves the original timestmap. The original timestamp is used to
        readjust the rest of the timestamps for the particular mutation.
    """

    def __init__(self):
        super(MutationTimeStampNormalizer, self).__init__()

    def sanitize(self, LogFile):
        for mi, mutation in enumerate(LogFile.mutations):
            for i, line in enumerate(mutation.data):
                if i == 0:
                    firstLineTimeStamp = mutation.data[i][0]
                    LogFile.mutations[mi].data[i][0] = '%g' % (float(LogFile.mutations[mi].data[i][0].replace(
                        ',', '.')) - float(firstLineTimeStamp.replace(',', '.')))
        return LogFile
