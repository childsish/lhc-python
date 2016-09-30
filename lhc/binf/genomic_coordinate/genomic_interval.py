from copy import deepcopy
from .genomic_position import GenomicPosition
from lhc.binf.sequence.reverse_complement import reverse_complement
from lhc.interval import Interval


class GenomicInterval(Interval):

    __slots__ = ('start', 'stop', 'data')

    def __init__(self, start, stop, *, chromosome=None, strand='+', data=None):
        """
        Create a genomic interval. Either provide two GenomicPositions or two integers and specify a chromosome.

        :param start: the start position of the interval (inclusive, 0-indexed)
        :type start: int | GenomicPosition
        :param stop: the stop position of the interval (not inclusive)
        :type stop: int | GenomicPosition
        :param str chromosome: chromosome identifier for interval
        :param str strand: either '+' or '-'
        :param data: extra data to be associated with the interval
        """
        if chromosome is not None:
            start = GenomicPosition(chromosome, start, strand)
            stop = GenomicPosition(chromosome, stop, strand)
        super().__init__(start, stop, data=data)

    def __str__(self):
        return '{}:{!r}-{!r}'.format(self.chromosome, self.start.position, self.stop.position)

    @property
    def chromosome(self):
        return self.start.chromosome

    @property
    def strand(self):
        return self.start.strand

    # Set-like operation functions

    def union(self, other):
        """
        Union of two intervals
        :param GenomicInterval other: interval to union with
        :return: union of two intervals íf overlapping or touching
        :rtype: GenomicInterval
        """
        interval = deepcopy(self)
        interval.union_update(other)
        return interval

    def union_update(self, other):
        """

        :param GenomicInterval other:
        :return:
        """
        self._assert_same_chromosome_and_strand(other)
        super().union_update(other)

    def intersect(self, other):
        interval = deepcopy(self)
        interval.intersect_update(other)
        return interval

    def intersect_update(self, other, compare_strand=True):
        self._assert_same_chromosome_and_strand(other)
        super().intersect_update(other)

    def difference(self, other):
        self._assert_same_chromosome_and_strand(other)
        if not self.overlaps(other):
            return Interval.INTERVAL_PAIR(self, None)

        left, right = None
        if self.start < other.start:
            left = GenomicInterval(self.chromosome, self.start.position, other.start.position,
                                   strand=self.strand, data=self.data)
        if other.stop < self.stop:
            right = GenomicInterval(self.chromosome, other.stop.position, self.stop.position,
                                    strand=self.strand, data=self.data)
        return Interval.INTERVAL_PAIR(left, right)

    # Interval arithmetic functions

    def add(self, other):
        self._assert_same_chromosome_and_strand(other)
        interval = super().add(other)
        return GenomicInterval(self.chromosome, interval.start.position, interval.stop.position,
                               strand=self.strand, data=self.data)

    def subtract(self, other):
        self._assert_same_chromosome_and_strand(other)
        interval = super().subtract(other)
        return GenomicInterval(self.chromosome, interval.start.position, interval.stop.position,
                               strand=self.strand, data=self.data)

    def multiply(self, other):
        self._assert_same_chromosome_and_strand(other)
        interval = super().multiply(other)
        return GenomicInterval(self.chromosome, interval.start.position, interval.stop.position,
                               strand=self.strand, data=self.data)

    def divide(self, other):
        self._assert_same_chromosome_and_strand(other)
        interval = super().divide(other)
        return GenomicInterval(self.chromosome, interval.start.position, interval.stop.position,
                               strand=self.strand, data=self.data)

    # Position functions

    def get_rel_pos(self, pos):
        if pos < self.start or pos >= self.stop:
            raise ValueError('Position outside interval bounds.')
        return pos - self.start if self.strand == '+'\
            else self.stop - pos - 1

    def get_sub_seq(self, sequence_set, fr=None, to=None):
        fr = self.start.position if fr is None else max(self.start.position, fr)
        to = self.stop.position if to is None else min(self.stop.position, to)
        res = sequence_set[self.chromosome][fr:to]  # if isinstance(sequence_set, dict) else sequence_set[fr:to]
        if self.strand == '-':
            res = reverse_complement(res)
        return res

    def get_5p(self):
        return self.start if self.strand == '+' else\
            self.stop

    def get_3p(self):
        return self.stop if self.strand == '+' else\
            self.start

    def _assert_same_chromosome_and_strand(self, other):
        if self.chromosome != other.chromosome or self.strand != other.strand:
            raise ValueError('Genomic intervals must be on same chromosome and strand.')

    def __getstate__(self):
        return self.start, self.stop, self.data

    def __setstate__(self, state):
        self.start, self.stop, self.data = state
