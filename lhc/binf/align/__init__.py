from lhc.binf.align.aligner import Aligner, DEFAULT_NUCLEOTIDE_ALPHABET, DEFAULT_NUCLEOTIDE_SCORING_MATRIX
from lhc.binf.align.alignment import Alignment
from lhc.binf.align.character_map import CharacterMap
from lhc.binf.align.global_alignment import GlobalAlignment
from lhc.binf.align.local_alignment import LocalAlignment
from lhc.binf.align.score import BLOSUM62, BLOSUM_ALPHABET, EDNA_ALPHABET, EDNA_SCORING_MATRIX
from lhc.binf.align.semiglobal_alignment import SemiGlobalAlignment


def align(sequence1: str, sequence2: str, mode=Aligner.Mode.GLOBAL):
    return Aligner(mode, DEFAULT_NUCLEOTIDE_SCORING_MATRIX, DEFAULT_NUCLEOTIDE_ALPHABET)\
        .align(sequence1, sequence2)
