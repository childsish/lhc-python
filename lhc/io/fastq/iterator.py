from collections import namedtuple
from itertools import islice


class FastqEntry(namedtuple('FastqEntry', ('hdr', 'seq', 'qual'))):
    def __str__(self):
        return '@{}\n{}\n{}+\n{}\n'.format(self.hdr, self.seq, self.qual_hdr, self.qual)


def iter_fastq(iterator):
    for hdr, seq, qual_hdr, qual in islice(iterator, start=0, stop=None, step=4):
        yield FastqEntry(hdr.strip()[1:], seq.strip(), qual.strip())
