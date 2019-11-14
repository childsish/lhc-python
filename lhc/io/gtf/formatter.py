from typing import IO
from lhc.binf.genomic_coordinate import GenomicInterval, GenomicIntervalFormatter


class GtfFormatter(GenomicIntervalFormatter):

    EXTENSIONS = ['.gtf', '.gtf.gz']

    def format(self, interval: GenomicInterval) -> str:
        return '{}\t.\t.\t{}\t{}\n'.format(interval.chromosome, interval.start.position, interval.stop.position)
