from contextlib import contextmanager
from typing import Optional
from .alignment_file import Alignment, AlignmentFile
from .fasta import FastaFile


def iter_sequences(filename, *, encoding='utf-8', format: Optional[str] = None):
    with open_alignment_file(filename, encoding=encoding, format=format) as sequences:
        yield from sequences


@contextmanager
def open_alignment_file(filename: Optional[str], mode='r', *, encoding='utf-8', format: Optional[str] = None):
    file = AlignmentFile.open_alignment_file(filename, mode, encoding=encoding, format=format)
    yield file


AlignmentFile.register_alignment_file(FastaFile)
