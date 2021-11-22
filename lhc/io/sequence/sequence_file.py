import pysam

from typing import ClassVar, Dict, Iterator, Optional
from lhc.binf.sequence import Sequence
from lhc.io import open_file


class SequenceFile:

    REGISTERED_EXTENSIONS = {}
    REGISTERED_FORMATS = {}  # type: Dict[str, ClassVar['SequenceFile']]

    def __init__(self, filename: str = None, mode: str = 'r', encoding: str = 'utf-8'):
        self.generator = None
        if 'r' in mode or 'w' in mode:
            self.generator = open_file(filename, mode, encoding)
            self.file = self.generator.__enter__()
        elif mode == 'q':
            self.file = pysam.FastaFile(filename)
        else:
            raise ValueError('Unrecognised open mode: {}'.format(mode))
        self.mode = mode
        self.encoding = encoding

    def __iter__(self) -> Iterator[Sequence]:
        if self.mode == 'w':
            raise ValueError('Sequence file opened for writing not reading.')

        return self.iter()

    def write(self, sequence: Sequence):
        if self.mode in 'rq':
            raise ValueError('Sequence file opened for reading or querying, not writing.')
        self.file.write(self.format(sequence))
        self.file.write('\n')

    def close(self):
        if self.mode in 'rw':
            self.file.close()

    def iter(self) -> Iterator[Sequence]:
        raise NotImplementedError('This function must be implemented by the subclass.')

    def format(self, sequence: Sequence) -> str:
        raise NotImplementedError('This function must be implemented by the subclass.')

    @classmethod
    def register_sequence_file(cls, loci_file: ClassVar['SequenceFile']):
        for extension in loci_file.EXTENSION:
            cls.REGISTERED_EXTENSIONS[extension] = loci_file.FORMAT
        cls.REGISTERED_FORMATS[loci_file.FORMAT] = loci_file

    @classmethod
    def open_sequence_file(
        cls,
        filename: Optional[str],
        mode='r',
        *,
        encoding='utf-8',
        format: Optional[str] = None
    ) -> 'SequenceFile':
        if filename is None and format is None:
            raise ValueError('When reading from stdin or writing to stdout, the file format must be specified.'
                             ' Valid formats are {}'.format(', '.join(cls.REGISTERED_FORMATS)))
        if not format:
            for extension, format in cls.REGISTERED_EXTENSIONS.items():
                if filename.endswith(extension):
                    break
        if format not in cls.REGISTERED_FORMATS:
            raise ValueError('Unknown loci file format: {}.'.format(format))
        return cls.REGISTERED_FORMATS[format](filename, mode, encoding)
