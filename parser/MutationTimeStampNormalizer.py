from LogFileSanitizer import LogFileSanitizer


class MutationTimeStampNormalizer(LogFileSanitizer):
    """MutationTimeStampNormalizer normalizes LogFile mutations timestamps
        to start from "0".

        Simply takes the first line, assing the timestamps of it to zero and
        saves the original timestamp. The original timestamp is used to
        readjust the rest of the timestamps for the particular mutation.
    """

    def __init__(self):
        super(MutationTimeStampNormalizer, self).__init__()

    def sanitize(self, LogFile):
        for mi, mutation in enumerate(LogFile.mutations):
            for i, (timestamp, event) in enumerate(mutation.data):
                if i == 0:
                    mutation_timestamp_delta = timestamp
                LogFile.mutations[mi].data[i][0] = '%g' % (float(LogFile.mutations[mi].data[i][0].replace(
                        ',', '.')) - float(mutation_timestamp_delta.replace(',', '.')))
        return LogFile
