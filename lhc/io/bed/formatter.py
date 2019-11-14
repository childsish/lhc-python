from typing import IO
from lhc.binf.genomic_coordinate import GenomicInterval, GenomicIntervalFormatter


class BedFormatter(GenomicIntervalFormatter):

    EXTENSIONS = ['.bed', '.bed.gz']

    def format(self, interval: GenomicInterval) -> str:
        return '{}\t{}\t{}\n'.format(interval.chromosome, interval.start.position, interval.stop.position)
