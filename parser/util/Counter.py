class Counter(object):
    """ Counter """

    def __init__(self):
        super(Counter, self).__init__()

    def countKeys(Log, key):
        count = 0
        for row in Log.data:
            if key in row:
                count = count + 1
        return count

    def countStartsWith(Log, key):
        count = 0
        for row in Log.data:
            timestamp, event = row
            if event.startswith(key):
                count = count + 1
        return count
