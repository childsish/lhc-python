from .locus_file import GenomicInterval, LocusFile


class RegionFile(LocusFile):

    EXTENSION = ('.txt', '.txt.gz')
    FORMAT = 'region'

    def parse(self, line: str, index=1) -> GenomicInterval:
        chromosome, interval = line.split(':', 1)
        start, end = interval.split('-')
        return GenomicInterval(int(start) - index, int(end), chromosome=chromosome)

    def format(self, interval: GenomicInterval, index=1) -> str:
        return '{chr}:{start}-{end}'.format(
            chr=interval.chromosome,
            start=interval.start.position + index,
            end=interval.end.position)
