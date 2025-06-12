from typing import ClassVar, Dict, Optional
from lhc.entities import NestedGenomicInterval
from lhc.io import open_file


class GeneFile:

    REGISTERED_EXTENSIONS = {}
    REGISTERED_FORMATS = {}  # type: Dict[str, ClassVar['GeneFile']]

    def __init__(self, filename: Optional[str] = None, mode: str = 'r', encoding: str = 'utf-8', index=1):
        self.generator = None
        if 'r' in mode or 'w' in mode:
            self.generator = open_file(filename, mode, encoding)
            self.file = self.generator.__enter__()
        else:
            raise ValueError('Unrecognised open mode: {}'.format(mode))
        self.mode = mode
        self.encoding = encoding
        self.index = index
    
    def __iter__(self):
        for line in self.file:
            if line and not line.startswith('#'):
                yield self.parse(line)

    def write(self, gene: NestedGenomicInterval):
        if self.mode in 'rq':
            raise ValueError('Gene file opened for reading or querying, not writing.')
        self.file.write(self.format(gene))
        self.file.write('\n')
    
    def iter(self):
        raise NotImplementedError
    
    def parse(self, entry) -> NestedGenomicInterval:
        raise NotImplementedError
    
    def format(self, gene: NestedGenomicInterval) -> str:
        raise NotImplementedError
    
    def close(self):
        self.file.close()
    
    @classmethod
    def register_gene_file(cls, genes_file: ClassVar['GeneFile']):
        for extension in genes_file.EXTENSION:
            cls.REGISTERED_EXTENSIONS[extension] = genes_file.FORMAT
        cls.REGISTERED_FORMATS[genes_file.FORMAT] = genes_file

    @classmethod
    def open_gene_file(
        cls,
        filename: Optional[str] = None,
        mode='r', *,
        encoding='utf-8',
        format: Optional[str] = None,
        index=1
    ) -> 'GeneFile':
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
            raise ValueError('Unknown gene file format: {}.'.format(format))
        return cls.REGISTERED_FORMATS[format](filename, mode, encoding, index)
