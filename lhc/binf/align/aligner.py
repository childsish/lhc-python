import numpy
import sys

from enum import Enum
from lhc.binf.align import CharacterMap, Alignment, GlobalAlignment, LocalAlignment, SemiGlobalAlignment

DEFAULT_NUCLEOTIDE_ALPHABET = 'ATGCSWRYKMBVHDN_'

DEFAULT_NUCLEOTIDE_SCORING_MATRIX = numpy.array([
    [ 5, -4, -4, -4, -4,  1,  1, -4, -4,  1, -4, -1, -1, -1, -2, -5],
    [-4,  5, -4, -4, -4,  1, -4,  1,  1, -4, -1, -4, -1, -1, -2, -5],
    [-4, -4,  5, -4,  1, -4,  1, -4,  1, -4, -1, -1, -4, -1, -2, -5],
    [-4, -4, -4,  5,  1, -4, -4,  1, -4,  1, -1, -1, -1, -4, -2, -5],
    [-4, -4,  1,  1, -1, -4, -2, -2, -2, -2, -1, -1, -3, -3, -1, -5],
    [ 1,  1, -4, -4, -4, -1, -2, -2, -2, -2, -3, -3, -1, -1, -1, -5],
    [ 1, -4,  1, -4, -2, -2, -1, -4, -2, -2, -3, -1, -3, -1, -1, -5],
    [-4,  1, -4,  1, -2, -2, -4, -1, -2, -2, -1, -3, -1, -3, -1, -5],
    [-4,  1,  1, -4, -2, -2, -2, -2, -1, -4, -1, -3, -3, -1, -1, -5],
    [ 1, -4, -4,  1, -2, -2, -2, -2, -4, -1, -3, -1, -1, -3, -1, -5],
    [-4, -1, -1, -1, -1, -3, -3, -1, -1, -3, -1, -2, -2, -2, -1, -5],
    [-1, -4, -1, -1, -1, -3, -1, -3, -3, -1, -2, -1, -2, -2, -1, -5],
    [-1, -1, -4, -1, -3, -1, -3, -1, -3, -1, -2, -2, -1, -2, -1, -5],
    [-1, -1, -1, -4, -3, -1, -1, -3, -1, -3, -2, -2, -2, -1, -1, -5],
    [-2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -5],
    [-5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5]])


class Aligner:

    class Mode(Enum):
        LOCAL = 1
        GLOBAL = 2
        SEMI = 3

    def __init__(self, mode: 'Aligner.Mode', scoring_matrix: numpy.array, alphabet=DEFAULT_NUCLEOTIDE_ALPHABET):
        if len(scoring_matrix) != len(alphabet) ** 2:
            raise ValueError('Scoring matrix must be square of alphabet length')
        self.mode = mode
        self.scoring_matrix = scoring_matrix
        self.character_map = CharacterMap(alphabet)

    def align(self, sequence1: str, sequence2: str) -> Alignment:
        end = 0 if self.mode == Aligner.Mode.LOCAL else sys.maxsize
        scores = [end, 0, 0, 0]

        alignment = SemiGlobalAlignment(sequence1, sequence2) if self.mode == Aligner.Mode.SEMI else \
            LocalAlignment(sequence1, sequence2) if self.mode == Aligner.Mode.LOCAL else \
            GlobalAlignment(sequence1, sequence2)
        s1 = self.character_map.translate(sequence1)
        s2 = self.character_map.translate(sequence2)
        gap = self.character_map.translate('_')[0]
        for i, ci in enumerate(s1):
            for j, cj in enumerate(s2):
                scores[Alignment.DIAG] = alignment.get_entry(i - 1, j - 1).score + self.scoring_matrix[ci, cj]
                scores[Alignment.LEFT] = alignment.get_entry(i, j - 1).score + self.scoring_matrix[gap, cj]
                scores[Alignment.UP] = alignment.get_entry(i - 1, j).score + self.scoring_matrix[ci, gap]
                idx = scores.index(max(scores))
                alignment.set_entry(i, j, scores[idx], idx)
        return alignment
