import gzip
import itertools
import os

from collections import namedtuple
from itertools import islice
from typing import Iterable, Optional, Union


class FastqEntry(namedtuple('FastqEntry', ('hdr', 'seq', 'qual'))):
    def __str__(self):
        return '@{}\n{}\n+\n{}\n'.format(self.hdr, self.seq, self.qual)


def iter_fastq(input: Union[str, Iterable]) -> Iterable[FastqEntry]:
    iterator = input
    if isinstance(input, str):
        iterator = gzip.open(input, 'rt') if input.endswith('.gz') else open(input)

    try:
        while True:
            hdr, seq, qual_hdr, qual = islice(iterator, 4)
            yield FastqEntry(hdr.strip()[1:], seq.strip(), qual.strip())
    except ValueError:
        raise StopIteration


def iter_partial_fastq(filename: str, fr: float, to: float):
    if fr < 0 or fr > 1 or to < 0 or to > 1:
        raise ValueError('fr and to must be between 0 and 1.')
    if fr >= to:
        raise ValueError('fr must be less than to.')

    try:
        with open(filename) as fileobj:
            statinfo = os.stat(filename)
            fileobj.seek(int(fr * statinfo.st_size))

            while fileobj.tell() / statinfo.st_size < to:
                hdr, seq, qual_hdr, qual = islice(fileobj, 4)
                yield FastqEntry(hdr.strip()[1:], seq.strip(), qual.strip())
    except ValueError:
        raise StopIteration
