class Alignment:
    def __init__(self, sequences):
        self.sequences = sequences

    def fetch(self, reference, start, stop):
        reference_sequence = self.sequences[reference]
        return {key: value[start:stop] for key, value in self.sequences.items()}
