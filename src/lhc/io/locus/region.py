from .locus_file import Locus, LocusFile


class RegionFile(LocusFile):

    EXTENSION = ('.txt', '.txt.gz')
    FORMAT = 'region'

    def parse(self, line: str, index=1) -> Locus:
        chromosome, interval = line.split(':', 1)
        start, end = interval.split('-')
        return Locus(int(start) - index, int(end), chromosome=chromosome)

    def format(self, interval: Locus, index=1) -> str:
        return '{chr}:{start}-{end}'.format(
            chr=interval.chromosome,
            start=interval.start.position + index,
            end=interval.end.position)
