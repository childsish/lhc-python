class Alignment:
    def __init__(self, sequences):
        self.sequences = sequences

    def fetch(self, start, stop):
        return {key: value[start:stop] for key, value in self.sequences.items()}
