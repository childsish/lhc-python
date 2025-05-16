class Alignment:
    def __init__(self, sequences):
        self.sequences = sequences

    def fetch(self, reference, start, end):
        reference_sequence = self.sequences[reference]
        reference_position = 0
        alignment_start = 0
        alignment_end = 0
        for alignment_position in range(len(reference_sequence)):
            reference_position += reference_sequence[alignment_position] != '-'
            if reference_position == start:
                alignment_start = alignment_position + 1
            if reference_position == end:
                alignment_end = alignment_position + 1
        return Alignment({key: value[alignment_start:alignment_end] for key, value in self.sequences.items()})
