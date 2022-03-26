from lhc.cli.align import Aligner, Mode, DEFAULT_NUCLEOTIDE_ALPHABET, DEFAULT_NUCLEOTIDE_SCORING_MATRIX


def align(sequence1: str, sequence2: str, mode=Mode.GLOBAL):
    aligner = Aligner(mode, DEFAULT_NUCLEOTIDE_SCORING_MATRIX, DEFAULT_NUCLEOTIDE_ALPHABET)
    return aligner.align(sequence1, sequence2)
