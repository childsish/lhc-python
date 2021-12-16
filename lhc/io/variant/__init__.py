from contextlib import contextmanager
from typing import Optional
from .variant_file import VariantFile
from .vcf import VcfFile


def iter_variants(filename, *, encoding='utf-8', format: Optional[str] = None, index=1):
    with open_variant_file(filename, encoding=encoding, format=format, index=index) as loci:
        yield from loci


@contextmanager
def open_variant_file(filename: Optional[str], mode='r', *, encoding='utf-8', format: Optional[str] = None, index=1):
    file = VariantFile.open_variant_file(filename, mode, encoding=encoding, format=format, index=index)
    yield file
    file.close()


VariantFile.register_variant_file(VcfFile)
