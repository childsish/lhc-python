from typing import Iterator
from .alignment_file import Alignment, AlignmentFile
from lhc.io.sequence import iter_sequences


class FastaFile(AlignmentFile):

    EXTENSION = ('.fasta', '.fa', '.fasta.gz', '.fa.gz')
    FORMAT = 'fasta'

    def iter(self) -> Iterator[Alignment]:
        yield Alignment({sequence.identifier: sequence.sequence for sequence in iter_sequences(self.filename, encoding=self.encoding)})

    def format(self, alignment: Alignment) -> str:
        return '\n'.join(f'>{key}\n{value}' for key, value in alignment.sequences.items())
