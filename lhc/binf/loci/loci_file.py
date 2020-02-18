from contextlib import contextmanager
from typing import Callable, Generator, Optional, IO, Union
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.io import open_file
from lhc.io.gff import iter_gff, format_gff
from lhc.io.gtf import iter_gtf, format_gtf
from lhc.io.region import iter_region, format_region


class LociWriter:
    def __init__(self, stream: IO, formatter: Callable[[GenomicInterval], str]):
        self.stream = stream
        self.formatter = formatter

    def write(self, loci: GenomicInterval):
        self.stream.write(self.formatter(loci))


@contextmanager
def open_loci_file(filename: Optional[str], mode='r', *, encoding='utf-8', format='region') -> Union[IO, Generator[GenomicInterval]]:
    with open_file(filename, mode, encoding) as fileobj:
        if 'w' in mode:
            format_function = format_gtf if format == 'gtf' or filename.endswith(('.gtf', '.gtf.gz')) else \
              format_gff if format == 'gff' or filename.endswith(('.gff', '.gff.gz')) else \
              format_region
            yield LociWriter(fileobj, format_function)
        else:
            iter_function = iter_gtf if format == 'gtf' or filename.endswith(('.gtf', '.gtf.gz')) else \
              iter_gff if format == 'gff' or filename.endswith(('.gff', '.gff.gz')) else \
              iter_region
            yield iter_function(fileobj)
