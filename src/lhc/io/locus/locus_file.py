from typing import ClassVar, Dict, Iterator, Optional
from lhc.entities.locus import Locus
from lhc.io import open_file


class LocusFile:

    REGISTERED_EXTENSIONS = {}
    REGISTERED_FORMATS = {}  # type: Dict[str, ClassVar['LocusFile']]

    def __init__(self, filename: Optional[str] = None, mode: str = 'r', encoding: str = 'utf-8', index=1):
        self.generator = None
        if 'r' in mode or 'w' in mode:
            self.generator = open_file(filename, mode, encoding)
            self.file = self.generator.__enter__()
        elif mode == 'q':
            import pysam
            self.file = pysam.TabixFile(filename)
        else:
            raise ValueError('Unrecognised open mode: {}'.format(mode))
        self.mode = mode
        self.encoding = encoding
        self.index = index

    def __iter__(self) -> Iterator[Locus]:
        if self.mode == 'w':
            raise ValueError('Locus file opened for writing, not reading.')
        for raw_entry in self.file:
            if line and not line.startswith('#'):
                yield self.parse(raw_entry, self.index)

    def fetch(self, locus: Locus) -> Iterator[Locus]:
        if self.mode in 'rw':
            raise ValueError('Loci file opened for reading or writing, not querying.')
        return (self.parse(raw_entry, self.index) for raw_entry in
                self.file.fetch(str(locus.chromosome), locus.start.position, locus.end.position))

    def write(self, locus: Locus):
        if self.mode in 'rq':
            raise ValueError('Locus file opened for reading or querying, not writing.')
        line = self.format(locus, self.index)
        self.file.write(self.format(locus, self.index))
        self.file.write('\n')

    def close(self):
        if self.mode in 'rw':
            self.file.close()

    def parse(self, raw_entry: str, index=1) -> Locus:
        raise NotImplementedError('This function must be implemented by the subclass.')

    def format(self, locus: Locus) -> str:
        raise NotImplementedError('This function must be implemented by the subclass.')

    @classmethod
    def register_locus_file(cls, loci_file: ClassVar['LocusFile']):
        for extension in loci_file.EXTENSION:
            cls.REGISTERED_EXTENSIONS[extension] = loci_file.FORMAT
        cls.REGISTERED_FORMATS[loci_file.FORMAT] = loci_file

    @classmethod
    def open_locus_file(
        cls,
        filename: Optional[str] = None,
        mode='r', *,
        encoding='utf-8',
        format: Optional[str] = None,
        index=1
    ) -> 'LocusFile':
        if not format:
            if filename is None:
                format = 'jsonl'
            else:
                for extension, format_ in cls.REGISTERED_EXTENSIONS.items():
                    if filename.endswith(extension):
                        format = format_
                if not format:
                    raise ValueError(f'Extension of file {filename} not registered.')
        if format not in cls.REGISTERED_FORMATS:
            raise ValueError('Unknown locus file format: {}.'.format(format))
        return cls.REGISTERED_FORMATS[format](filename, mode, encoding, index)
