from functools import total_ordering
from lhc.misc.natural_key import natural_key


class ChromosomeIdentifier:
    def __init__(self, chromosome: str):
        self.chromosome = chromosome
        self.parts = tuple(natural_key(chromosome))

    def __str__(self):
        return self.chromosome

    def __hash__(self):
        return hash(self.chromosome)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.chromosome == other
        return self.parts == other.parts

    def __lt__(self, other):
        if isinstance(other, str):
            return self.chromosome < other
        return self.parts < other.parts


@total_ordering
class GenomicPosition:

    def __init__(self, position, *, chromosome=None, strand='+', data=None):
        self.chromosome = None if chromosome is None else chromosome if isinstance(chromosome, ChromosomeIdentifier) else ChromosomeIdentifier(chromosome)
        self.position = position
        self.strand = strand
        self.data = data

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return 'GenomicPosition({})'.format(self)

    def __hash__(self):
        return hash((self.chromosome, self.position))

    def __eq__(self, other):
        if isinstance(other, int) or self.chromosome is None or other.chromosome is None:
            return self.position == other
        return self.chromosome == other.chromosome and self.position == other.position and\
            self.strand == other.strand

    def __lt__(self, other):
        if isinstance(other, int) or self.chromosome is None or other.chromosome is None:
            return self.position < other
        return (self.chromosome < other.chromosome) or\
            (self.chromosome == other.chromosome) and (self.position < other.position)

    def __add__(self, other):
        """
        Add an integer to the current position
        :param int other: integer to add
        :return: new position
        :rtype: GenomicPosition
        """
        return GenomicPosition(self.position + other, chromosome=self.chromosome, strand=self.strand)

    def __sub__(self, other):
        """
        Subtract either an integer from the current position
        :param int other: integer to subtract
        :return: new position
        :rtype: GenomicPosition
        """
        if isinstance(other, GenomicPosition):
            return self.get_distance_to(other)
        return GenomicPosition(self.position - other, chromosome=self.chromosome, strand=self.strand)

    def __truediv__(self, other: int):
        return self.position / other

    def get_distance_to(self, other):
        """
        Get the distance between two positions
        :param GenomicPosition other: other position
        :return: distance between positions
        :rtype: int
        """
        if self.chromosome != other.chromosome:
            raise ValueError('Positions on different chromosomes: "{}" and "{}"'.format(self.chromosome, other.chromosome))
        return self.position - other.position
