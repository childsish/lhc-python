from collections import namedtuple
from itertools import islice


class FastqEntry(namedtuple('FastqEntry', ('hdr', 'seq', 'qual'))):
    def __str__(self):
        return '@{}\n{}\n+\n{}\n'.format(self.hdr, self.seq, self.qual)


def iter_fastq(iterator):
    try:
        while True:
            hdr, seq, qual_hdr, qual = islice(iterator, 4)
            yield FastqEntry(hdr.strip()[1:], seq.strip(), qual.strip())
    except ValueError:
        raise StopIteration
