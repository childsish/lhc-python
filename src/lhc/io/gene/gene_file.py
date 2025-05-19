from lhc.entities.gene import Gene

class GeneFile:
    def __iter__(self):
        for entry in self.iter():
            yield self.parse(entry)
    
    def iter(self):
        raise NotImplementedError
    
    def parse(self, entry) -> Gene:
        raise NotImplementedError
    
    def format(self, gene: Gene) -> str:
        raise NotImplementedError
    
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
        if filename is None and format is None:
            raise ValueError('When reading from stdin or writing to stdout, the file format must be specified.'
                             ' Valid formats are {}'.format(', '.join(cls.REGISTERED_FORMATS)))
        if not format:
            for extension, format in cls.REGISTERED_EXTENSIONS.items():
                if filename.endswith(extension):
                    break
        if format not in cls.REGISTERED_FORMATS:
            raise ValueError('Unknown gene file format: {}.'.format(format))
        return cls.REGISTERED_FORMATS[format](filename, mode, encoding, index)
