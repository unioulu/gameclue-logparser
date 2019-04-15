class Mutation(object):
    """
    Mutation represents a mutation part of a LogFile.

    Ex: mutation = Mutation(data, 'base')
    """

    def __init__(self, name, data):
        super(Mutation, self).__init__()
        self.name = name
        self.data = data
