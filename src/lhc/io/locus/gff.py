from .locus_file import Locus, LocusFile
from lhc.entities.interval import Interval
from lhc.io.parsers.gff import parse_gff


class GffFile(LocusFile):

    EXTENSION = ('.gff', '.gff.gz', '.gff3', '.gff3.gz')
    FORMAT = 'gff'

    def parse(self, line: str, index=1) -> Locus:
        return parse_gff(line, index)

    def format(self, locus: Locus, index=1) -> str:
        attrs = {key: value for key, value in locus.data.items() if key not in {'source', 'feature', 'score', 'frame'}}
        return '{chr}\t{data[source]}\t{data[feature]}\t{start}\t{end}\t{data[score]}\t{strand}\t{data[frame]}\t{attrs}'.format(
            chr=locus.chromosome,
            start=locus.interval.start + index,
            end=locus.interval.end,
            strand=locus.strand,
            data=locus.data,
            attrs=';'.join('{}={}'.format(key, value) for key, value in attrs.items()))

