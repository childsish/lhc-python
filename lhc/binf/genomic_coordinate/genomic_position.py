class GenomicPosition(object):

    def __init__(self, chromosome, position, strand='+'):
        self.chromosome = chromosome
        self.position = position
        self.strand = strand

    def __str__(self):
        return '{}:{}'.format(self.chromosome, self.position + 1)

    def __eq__(self, other):
        return self.chromosome == other.chromosome and self.position == other.position and\
            self.strand == other.strand

    def __lt__(self, other):
        return (self.chromosome < other.chromosome) or\
            (self.chromosome == other.chromosome) and (self.position < other.pos)

    def __add__(self, other):
        """
        Add to position
        :param other: amount to add
        :type other: int
        :return: new position
        :rtype: GenomicPosition
        """
        return GenomicPosition(self.chromosome, self.position + other, self.strand)

    def __sub__(self, other):
        """
        Subtract two positions from each other
        :param other: other position
        :type other: GenomicPosition
        :return: distance between positions
        :rtype: int
        """
        if self.chromosome != other.chromosome:
            raise ValueError('Positions not on same chromosome')
        return other.position - self.position
