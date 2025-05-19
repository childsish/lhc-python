from lhc.entities.interval import Interval
from .locus_file import Locus, LocusFile


class GffFile(LocusFile):

    EXTENSION = ('.gff', '.gff.gz', '.gff3', '.gff3.gz')
    FORMAT = 'gff'

    def parse(self, line: str, index=1) -> Locus:
        parts = line.rstrip('\r\n').split('\t')
        attributes = self.parse_attributes(parts[8])
        attributes['source'] = parts[1],
        attributes['feature'] = parts[2]
        attributes['score'] = parts[5]
        attributes['frame'] = parts[7]
        return Locus(
            chromosome=parts[0],
            interval=Interval(int(parts[3]) - index, int(parts[4])),
            strand=parts[6],
            data=attributes,
        )

    def format(self, interval: Locus, index=1) -> str:
        attrs = {key: value for key, value in interval.data.items() if key not in {'source', 'feature', 'score', 'frame'}}
        return '{chr}\t{data[source]}\t{data[feature]}\t{start}\t{end}\t{data[score]}\t{strand}\t{data[frame]}\t{attrs}'.format(
            chr=interval.chromosome,
            start=interval.start.position + index,
            end=interval.end.position,
            strand=interval.strand,
            data=interval.data,
            attrs=';'.join('{}={}'.format(key, value) for key, value in attrs.items()))

    @staticmethod
    def parse_attributes(line):
        attributes = {}
        for part in line.split(';'):
            if part:
                key, value = part.split('=', 1) if '=' in part else part
                attributes[key] = value.split(',')
        return attributes
