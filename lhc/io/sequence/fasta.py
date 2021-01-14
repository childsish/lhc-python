from typing import Iterator
from .sequence_file import Sequence, SequenceFile


class FastaFile(SequenceFile):

    EXTENSION = ('.fasta', '.fa', '.fasta.gz', '.fa.gz')
    FORMAT = 'fasta'

    def iter(self) -> Iterator[Sequence]:
        line = next(self.file)
        while line:
            if line.startswith('#'):
                continue
            elif not line.startswith('>'):
                raise ValueError('Invalid fasta file format.')

            header = line.strip()[1:]
            identifier = header.split(maxsplit=1)[0]
            sequence = []
            for line in self.file:
                if line == '' or line.startswith('>'):
                    yield Sequence(identifier, ''.join(sequence), data=header)
                    del sequence[:]
                else:
                    sequence.append(line.strip())

    def format(self, sequence: Sequence) -> str:
        return '{}\n{}'.format(sequence.identifier, sequence)
