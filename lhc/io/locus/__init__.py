from contextlib import contextmanager
from typing import Optional
from .locus_file import LocusFile
from .bed import BedFile
from .gff import GffFile
from .gtf import GtfFile
from .paf import PafFile
from .sam import SamFile
from .region import RegionFile
from .repeat_masker import RepeatMaskerFile


def iter_loci(filename, *, encoding='utf-8', format: Optional[str] = None, index=1):
    with open_locus_file(filename, encoding=encoding, format=format, index=index) as loci:
        yield from loci


@contextmanager
def open_locus_file(filename: Optional[str], mode='r', *, encoding='utf-8', format: Optional[str] = None, index=1):
    file = LocusFile.open_loci_file(filename, mode, encoding=encoding, format=format, index=index)
    yield file
    file.close()


LocusFile.register_loci_file(BedFile)
LocusFile.register_loci_file(GffFile)
LocusFile.register_loci_file(GtfFile)
LocusFile.register_loci_file(PafFile)
LocusFile.register_loci_file(RegionFile)
LocusFile.register_loci_file(RepeatMaskerFile)
