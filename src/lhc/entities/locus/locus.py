from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Optional
from .genomic_position import GenomicPosition
from lhc.entities.sequence.reverse_complement import reverse_complement
from lhc.entities.interval import Interval, IntervalSplit


@dataclass(frozen=True, order=True, slots=True)
class Locus:
    
    chromosome: str
    interval: Interval
    strand: Optional[str] = None
    data: Dict[any, any] = field(default_factory=dict)

    def __post_init__(self):
        if self.strand not in (None, '+', '-'):
            raise ValueError(f"strand must be '+' or '-' or None, got {self.strand!r}")

    def __str__(self):
        return '{}:{!r}-{!r}'.format(self.chromosome, self.interval.start + 1, self.interval.end)

    def switch_strand(self):
        return Locus(self.chromosome, self.interval, '-' if self.start.strand == '+' else '+', self.data)

    # Set-like operation functions

    def union(self, other: 'Locus', *, ignore_strand=False) -> 'Locus':
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        interval = self.interval.union(other.interval)
        if interval is None:
            return None
        return Locus(self.chromosome, interval, self.strand, dict(self.data))

    def intersect(self, other: 'Locus', *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        interval = self.interval.intersect(other.interval)
        if interval is None:
            return None
        return Locus(self.chromosome, interval, self.strand, dict(self.data))

    def difference(self, other: 'Locus', *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        interval_split = self.interval.difference(other.interval)
        left = None
        if interval_split.left is not None:
            left = Locus(self.chromosome, interval_split.left, self.strand, dict(self.data))
        right = None
        if interval_split.right is not None:
            right = Locus(self.chromosome, interval_split.right, self.strand, dict(self.data))
        return IntervalSplit(left, right)

    # Interval arithmetic functions

    def add(self, other: 'Locus', *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        interval = self.interval.add(other.interval)
        if interval is None:
            return None
        return Locus(self.chromosome, interval, self.strand, dict(self.data))

    def subtract(self, other: 'Locus', *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        interval = self.interval.subtract(other.interval)
        if interval is None:
            return None
        return Locus(self.chromosome, interval, self.strand, dict(self.data))

    def multiply(self, other: 'Locus', *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        interval = self.interval.multiply(other.interval)
        if interval is None:
            return None
        return Locus(self.chromosome, interval, self.strand, dict(self.data))

    def divide(self, other: 'Locus', *, ignore_strand=False):
        if not ignore_strand:
            self._assert_same_chromosome_and_strand(other)
        interval = self.interval.divide(other.interval)
        if interval is None:
            return None
        return Locus(self.chromosome, interval, self.strand, dict(self.data))

    # Position functions

    def get_rel_pos(self, pos: int):
        if pos < self.interval.start or pos >= self.interval.end:
            raise ValueError('Position outside interval bounds.')
        return pos - self.interval.start if self.strand == '+'\
            else self.end - pos - 1

    def get_sub_seq(self, sequence_set, fr=None, to=None):
        fr = self.interval.start if fr is None else max(self.interval.start, fr)
        to = self.interval.end if to is None else min(self.interval.end, to)
        res = sequence_set.fetch(str(self.chromosome), fr, to)
        if self.strand == '-':
            res = reverse_complement(res)
        return res

    def get_5p(self):
        return self.interval.start if self.strand == '+' else\
            self.interval.end

    def get_3p(self):
        return self.interval.end if self.strand == '+' else\
            self.interval.start

    def _assert_same_chromosome_and_strand(self, other):
        if self.chromosome != other.chromosome or self.strand != other.strand:
            raise ValueError('Genomic intervals must be on same chromosome and strand.')

