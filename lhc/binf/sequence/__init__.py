class Sequence:
    def __init__(self, identifier, sequence, *, data=None):
        self.identifier = identifier
        self.sequence = sequence
        self.data = {} if data is None else data

    def __str__(self):
        return self.sequence
