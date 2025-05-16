import dataclasses
import functools

from typing import Any, Optional


@dataclasses.dataclass
class IntervalPair:
    left: Optional['Interval'] = None
    right: Optional['Interval'] = None

    def __iter__(self):
        yield self.left
        yield self.right


@functools.total_ordering
class Interval(object):

    __slots__ = 'start', 'end', 'data'

    def __init__(self, start, end, *, data: Any = None):
        self.start, self.end = sorted((start, end))
        self.data = data

    def __str__(self) -> str:
        return f'[{self.start}, {self.end})'

    def __repr__(self) -> str:
        return f'Interval({self.start}, {self.end})'
    
    def __len__(self) -> int:
        return self.end - self.start
    
    def __eq__(self, other: 'Interval') -> bool:
        return self.start == other.start and self.end == other.end
    
    def __lt__(self, other: 'Interval') -> bool:
        return self.end < other.end if self.start == other.start else self.start < other.start
    
    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __contains__(self, item) -> bool:
        return self.start <= item < self.end if self.start != self.end else self.start == item
        
    # Relative location functions

    def overlaps(self, other: 'Interval') -> bool:
        """Test if self overlaps other

        :param Interval other: interval being tested
        :rtype: bool
        """
        return self.start < other.end and other.start < self.end
    
    def contains(self, other: 'Interval') -> bool:
        """Test if self wholly contains other

        :param Interval other: interval being tested
        :rtype: bool
        """
        return self.start <= other.start and other.end <= self.end
    
    def touches(self, other: 'Interval') -> bool:
        """Test if self touches (but doesn't overlap) other

        :param Interval other: interval being tested
        :rtype: bool
        """
        return self.start == other.end or self.end == other.start
    
    # Set-like operation functions
    
    def union(self, other: 'Interval') -> Optional['Interval']:
        """Return the interval covering self and other if they overlap

        :param Interval other: interval to union with
        :rtype: Interval or None
        """
        return Interval(min(self.start, other.start), max(self.end, other.end))\
            if self.overlaps(other) or self.touches(other) else None
    
    def intersect(self, other: 'Interval') -> Optional['Interval']:
        """Return an interval where self and other intersect

        :param Interval other: interval to intersect with
        :rtype: Interval or None 
        """
        return Interval(max(self.start, other.start), min(self.end, other.end))\
            if self.overlaps(other) else None
    
    def difference(self, other: 'Interval') -> IntervalPair:
        """Return an interval that covers self but not other

        :param Interval other: interval to difference wit
        :rtype: 2-tuple of interval or None
        
        If there is no overlap, the result is at .left and .right is None
        If self is cut on the lower side, the result is at .right.
        If self is cut on the upper side, the result is at .left.
        If self is cut in the middle, the result in in both .left and .right
        """
        if not self.overlaps(other):
            return IntervalPair(self)
        
        left, right = None, None
        if self.start < other.start:
            left = Interval(self.start, other.start)
        if other.end < self.end:
            right = Interval(other.end, self.end)
        return IntervalPair(left, right)
    
    # Interval arithmetic functions
    
    def add(self, other: 'Interval') -> 'Interval':
        """Return the arithmetic addition of self and other

        :param Interval other: the other interval
        """
        return Interval(self.start + other.start, self.end + other.end)
    
    def subtract(self, other: 'Interval') -> 'Interval':
        """Return the arithmetic subtraction of self and other
        
        :param Interval other: the other interval
        """
        return Interval(self.start - other.end, self.end - other.start)
    
    def multiply(self, other: 'Interval') -> 'Interval':
        """Return the arithmetic multiplication of self and other
        
        :param Interval other: the other interval
        """
        return Interval(min(self.start * other.start, self.start * other.end,
                            self.end * other.start, self.end * other.end),
                        max(self.start * other.start, self.start * other.end,
                            self.end * other.start, self.end * other.end))
    
    def divide(self, other: 'Interval') -> Optional['Interval']:
        """Return the arithmetic division of self and other
        
        :param Interval other: the other interval
        """
        return Interval(min(self.start / other.start, self.start / other.end,
                            self.end / other.start, self.end / other.end), 
                        max(self.start / other.start, self.start / other.end,
                            self.end / other.start, self.end / other.end))\
            if other.start != 0 and other.end != 0 else None
    
    # Position functions
    
    def get_abs_pos(self, pos: int) -> int:
        """Get the absolute position of a position relative to a interval
        
        :param int pos: the position relative to the interval
        """
        if pos < 0 or pos >= self.end - self.start:
            raise IndexError(f'Relative position {pos} is not contained within {self}')
        return self.start + pos
    
    def get_rel_pos(self, pos: int) -> int:
        """Get the position relative to a interval of a position.
    
        :param int pos: the position to calculate relative to the interval
        """
        if pos < self.start or pos >= self.end:
            raise IndexError(f'Absolute position {pos} is not contained within {self}')
        return pos - self.start
    
    # Sequence functions
    
    def get_sub_seq(self, seq: str) -> str:
        """Get the subsequence

        :param str seq: sequences to get subsequence from
        :rtype: str
        """
        return seq[self.start:self.end]

    def __getstate__(self):
        return self.start, self.end, self.data

    def __setstate__(self, state):
        self.start, self.end, self.data = state
