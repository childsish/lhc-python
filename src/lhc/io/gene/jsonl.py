import string

from json import loads, dumps

from .gene_file import GeneFile
from lhc.entities import NestedGenomicInterval


class JsonLFile(GeneFile):

    EXTENSION = ('.json', '.json.gz')
    FORMAT = 'jsonl'
    
    def iter(self):
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError

    def format(self, gene: NestedGenomicInterval, index=1) -> str:
        raise NotImplementedError
