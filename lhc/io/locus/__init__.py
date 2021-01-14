from contextlib import contextmanager
from typing import Optional
from .loci_file import LociFile
from .bed import BedFile
from .gff import GffFile
from .gtf import GtfFile
from .paf import PafFile
from .sam import SamFile
from .region import RegionFile
from .repeat_masker import RepeatMaskerFile


def iter_loci(filename, *, encoding='utf-8', format: Optional[str] = None, index=1):
    with open_loci_file(filename, encoding=encoding, format=format, index=index) as loci:
        yield from loci


@contextmanager
def open_loci_file(filename: Optional[str], mode='r', *, encoding='utf-8', format: Optional[str] = None, index=1):
    file = LociFile.open_loci_file(filename, mode, encoding=encoding, format=format, index=index)
    yield file
    file.close()


LociFile.register_loci_file(BedFile)
LociFile.register_loci_file(GffFile)
LociFile.register_loci_file(GtfFile)
LociFile.register_loci_file(PafFile)
LociFile.register_loci_file(RegionFile)
LociFile.register_loci_file(RepeatMaskerFile)
