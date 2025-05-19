from contextlib import contextmanager
from typing import Optional
from .gene_file import GeneFile
from .gff import GffFile

def iter_genes(filename, *, encoding='utf-8', format: Optional[str] = None, index=1):
    with open_gene_file(filename, encoding=encoding, format=format, index=index) as genes:
        yield from genes


@contextmanager
def open_gene_file(filename: Optional[str] = None, mode='r', *, encoding='utf-8', format: Optional[str] = None, index=1):
    file = GeneFile.open_gene_file(filename, mode, encoding=encoding, format=format, index=index)
    yield file
    file.close()


LocusFile.register_locus_file(GffFile)
