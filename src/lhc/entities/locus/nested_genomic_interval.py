from typing import List

from functools import total_ordering
from .locus import Locus
from lhc.entities.interval import Interval
from lhc.entities.sequence.reverse_complement import reverse_complement


@total_ordering
class NestedGenomicInterval:
    def __init__(self, chromosome, interval, strand, data=None):
        self.locus = Locus(chromosome, interval, strand, data)
        self.parent = None
        self.children = []  # type: List['NestedGenomicInterval']

    def __str__(self):
        if self.chromosome is None:
            return '{}-{}'.format(self.start.position, self.end.position)
        return '{}:{}-{}'.format(self.chromosome, self.start.position, self.end.position)

    def __repr__(self):
        return 'NestedGenomicInterval({})'.format(self)

    def __len__(self):
        if len(self.children) == 0:
            return self.locus.interval.end - self.locus.interval.start
        return sum(len(child) for child in self.children)
    
    def __eq__(self, other: 'NestedGenomicInterval') -> bool:
        return self.locus == other.locus
    
    def __lt__(self, other: 'NestedGenomicInterval') -> bool:
        return self.locus < other.locus

    def add_child(self, child: 'NestedGenomicInterval'):
        child.parent = self
        self.children.append(child)
        if child.locus.interval.start < self.locus.interval.start:
            self.locus.interval.start = child.locus.interval.start
            if self.parent:
                self.parent.locus.interval.start = child.locus.interval.start
        if child.locus.interval.end > self.locus.interval.end:
            self.locus = Locus(self.locus.chromosome, Interval(self.locus.interval.start, child.locus.interval.end), self.locus.strand, self.locus.data)
            if self.parent:
                self.parent.locus = Locus(self.locus.chromosome, Interval(self.parent.locus.interval.start, child.locus.interval.end), self.parent.locus.strand, self.parent.locus.data)

    def switch_strand(self):
        super().switch_strand()
        for child in self.children:
            child.switch_strand()

    # Position functions
    
    def get_abs_pos(self, pos):
        intervals = self.children if self.strand == '+' else reversed(self.children)
        fr = 0
        for interval in intervals:
            length = len(interval)
            if fr <= pos < fr + length:
                return interval.get_abs_pos(pos - fr)
            fr += length
        raise IndexError('relative position {} not contained within {}'.format(pos, self))
    
    def get_rel_pos(self, pos, types=None):
        if len(self.children) == 0:
            if types is None or self.data['type'] in types:
                return pos - self.start.position
            else:
                raise ValueError('Position in interval but not of right type.')

        rel_pos = 0
        intervals = iter(self.children) if self.strand == '+' else reversed(self.children)
        for interval in intervals:
            if interval.start.position <= pos < interval.end.position:
                return rel_pos + interval.get_rel_pos(pos, types=types)
            if types is None or interval.data['type'] in types:
                rel_pos += len(interval)
        raise IndexError('absolute position {} not contained within {}'.format(pos, self))
    
    # Sequence functions
    
    def get_sub_seq(self, sequence_set, *, types=None):
        res = ''
        if len(self.children) > 0:
            res = ''.join(child.get_sub_seq(sequence_set, types=types) for child in self.children)
            if self.strand == '-':
                res = reverse_complement(res)
        elif types is None or self.data['type'] in types:
            res = super().get_sub_seq(sequence_set)
        return res

    def get_5p(self):
        return self.children[0].get_5p() if self.strand == '+' else\
            self.children[-1].get_5p()

    def get_3p(self):
        return self.children[-1].get_3p() if self.strand == '+' else\
            self.children[0].get_3p()
