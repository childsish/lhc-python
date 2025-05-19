from copy import deepcopy
from dataclasses import dataclass
from .genomic_position import GenomicPosition
from lhc.entities.sequence.reverse_complement import reverse_complement
from lhc.entities.interval import Interval


@dataclass(frozen=True, order=True, slots=True)
class Locus(Interval):
    
    data: dict[any, any]

    def __init__(self, start, end, *, chromosome=None, strand='+', data=None):
        """
        Create a genomic interval. Either provide two GenomicPositions or two integers and specify a chromosome.

        :param start: the start position of the interval (inclusive, 0-indexed)
        :type start: int | GenomicPosition
        :param end: the end position of the interval (not inclusive)
        :type end: int | GenomicPosition
        :param str chromosome: chromosome identifier for interval
        :param str strand: either '+' or '-'
        :param data: extra data to be associated with the interval
        """
        start = start if isinstance(start, GenomicPosition) else GenomicPosition(start, chromosome=chromosome, strand=strand)
        end = end if isinstance(end, GenomicPosition) else GenomicPosition(end, chromosome=chromosome, strand=strand)
        Interval.__init__(self, start, end)
        object.__setattr__(self, 'data', data or {})

    def __str__(self):
        return '{}:{!r}-{!r}'.format(self.chromosome, self.start.position + 1, self.end.position)

    @property
    def chromosome(self):
        return self.start.chromosome

    @chromosome.setter
    def chromosome(self, chromosome):
        self.start.chromosome = chromosome
        self.end.chromosome = chromosome

    @property
    def strand(self):
        return self.start.strand

    def switch_strand(self):
        strand = '-' if self.start.strand == '+' else '+'
        self.start.strand = strand
        self.end.strand = strand

    # Set-like operation functions

    def union(self, other, *, ignore_strand=False) -> 'Locus':
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        return super().union(other)

    def intersect(self, other, *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        return super().intersect(other)

    def difference(self, other, *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        return super().difference(other)

    # Interval arithmetic functions

    def add(self, other, *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        return super().add(other)

    def subtract(self, other, *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        return super().subtract(other)

    def multiply(self, other, *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        return super().multiply(other)

    def divide(self, other, *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        return super().divide(other)

    # Position functions

    def get_rel_pos(self, pos):
        if pos < self.start or pos >= self.end:
            raise ValueError('Position outside interval bounds.')
        return pos - self.start if self.strand == '+'\
            else self.end - pos - 1

    def get_sub_seq(self, sequence_set, fr=None, to=None):
        fr = self.start.position if fr is None else max(self.start.position, fr)
        to = self.end.position if to is None else min(self.end.position, to)
        res = sequence_set.fetch(str(self.chromosome), fr, to)
        if self.strand == '-':
            res = reverse_complement(res)
        return res

    def get_5p(self):
        return self.start if self.strand == '+' else\
            self.end

    def get_3p(self):
        return self.end if self.strand == '+' else\
            self.start

    def _assert_same_chromosome_and_strand(self, other):
        if self.chromosome != other.chromosome or self.strand != other.strand:
            raise ValueError('Genomic intervals must be on same chromosome and strand.')

