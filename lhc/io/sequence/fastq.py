from itertools import islice
from typing import Iterator
from .sequence_file import Sequence, SequenceFile


class FastqFile(SequenceFile):

    EXTENSION = ('.fastq', '.fq', '.fastq.gz', '.fq.gz')
    FORMAT = 'fastq'

    def iter(self) -> Iterator[Sequence]:
        try:
            while True:
                hdr, seq, qual_hdr, qual = islice(self.file, 4)
                yield Sequence(hdr.strip()[1:], seq.strip(), data=qual.strip())
        except ValueError:
            raise StopIteration

    def format(self, sequence: Sequence) -> str:
        return '{}\n{}\n{}\n{}'.format(sequence.identifier, sequence, sequence.identifier, sequence.data)
