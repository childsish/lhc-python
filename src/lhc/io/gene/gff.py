from .gene_file import GeneFile


class GffFile(GeneFile):
    def iter(self):
        raise NotImplementedError

    def parse(self, entry):
        raise NotImplementedError
    
    def format(self, gene: Gene):
        raise NotImplementedError
