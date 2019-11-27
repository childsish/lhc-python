from typing import Iterable, Iterator
from lhc.binf.genomic_coordinate import GenomicInterval, GenomicIntervalConverter


class RepeatMaskerConverter(GenomicIntervalConverter):

    COLUMNS = ['score', 'divergence', 'deletion', 'insertion', 'chromosome', 'start', 'end', 'query_left', 'strand',
               'subfamily', 'class/family', 'match_start', 'match_end', 'match_left', 'id']
    EXTENSIONS = ['.fa.out', '.fa.out.gz']

    def __init__(self, lines: Iterator[str]):
        self.lines = lines

    def __iter__(self) -> Iterable[GenomicInterval]:
        next(self.lines)
        next(self.lines)
        next(self.lines)
        for line in self.lines:
            yield self.parse(line)

    def parse(self, line):
        parts = line.rstrip('\r\n').split()
        class_, *family = parts[10].split('/', 1)
        return GenomicInterval(
            int(parts[5]) - 1,
            int(parts[6]),
            chromosome=parts[4],
            strand='+' if parts[8] == '+' else '-',
            data={'score': parts[0], 'divergence': parts[1], 'deletion': parts[2], 'insertion': parts[3],
                  'query_left': parts[7], 'subfamily_id': parts[9], 'class_id': class_, 'family_id': ''.join(family),
                  'match_start': parts[12], 'match_end': parts[13], 'match_left': parts[11], 'transcript_id': parts[12],
                  'source': 'RepeatMasker', 'feature': 'repeat_element', 'frame': '0'})

    def format(self, interval: GenomicInterval):
        raise NotImplementedError('This function has not yet been implemented.')
