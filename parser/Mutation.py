class Mutation(object):
    """
    Mutation represents a (mutation) part of a LogFile.
    """

    def __init__(self, name, data, played_in_order):
        super(Mutation, self).__init__()
        self.name = name
        self.data = data
        self.played_in_order = played_in_order
