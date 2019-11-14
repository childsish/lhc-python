from typing import Iterable
from lhc.binf.genomic_coordinate import GenomicInterval, GenomicIntervalConverter


class GtfConverter(GenomicIntervalConverter):

    COLUMNS = ['chromosome', 'source', 'feature', 'start', 'stop', 'score', 'strand', 'frame', 'attribute']
    EXTENSIONS = ['.gtf', '.gtf.gz']

    def __init__(self, lines: Iterable[str]):
        self.lines = lines

    def __iter__(self) -> Iterable[GenomicInterval]:
        for line in self.lines:
            yield self.parse(line)

    def parse(self, line) -> GenomicInterval:
        parts = line.rstrip('r\n').split('\t')
        return GenomicInterval(int(parts[3]) - 1, int(parts[4]),
                               chromosome=parts[0],
                               strand=parts[6],
                               data={
                                   'source': parts[1],
                                   'type': parts[2],
                                   'score': parts[5],
                                   'phase': parts[7],
                                   'attr': GtfConverter.parse_attributes(parts[8])
                               })

    @staticmethod
    def parse_attributes(line):
        parts = (part.strip() for part in line.split(';'))
        parts = [part.split(' ', 1) for part in parts if part != '']
        for part in parts:
            part[1] = part[1][1:-1] if part[1].startswith('"') else int(part[1])
        return dict(parts)

    def format(self, interval: GenomicInterval):
        return '{}\t.\t.\t{}\t{}\n'.format(interval.chromosome, interval.start.position + 1, interval.stop.position)
