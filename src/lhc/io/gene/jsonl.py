import string

from json import loads, dumps
from typing import Any, Dict

from .gene_file import GeneFile
from lhc.entities import NestedGenomicInterval


class JsonLFile(GeneFile):

    EXTENSION = ('.json', '.json.gz')
    FORMAT = 'jsonl'
    
    def __iter__(self) -> NestedGenomicInterval:
        for line in self.file:
            d = json.loads(json_str)
            return self._dict_to_gene(d)

    def format(self, node: NestedGenomicInterval, index=0) -> str:
        return dumps(self._gene_to_dict(node, index))

    def _dict_to_gene(self, d: Dict[str, Any]) -> NestedGenomicInterval:
        # create the node itself
        node = NestedGenomicInterval(
            chromosome=d['chromosome'],
            interval=Interval(d['start'], d['end']),
            strand=d['strand'],
            data=d.get('data')
        )

        # recursively reconstruct children and attach them
        for child_dict in d.get('children', []):
            child = self._dict_to_gene(child_dict)
            node.add_child(child)

        return node

    def _gene_to_dict(self, gene: NestedGenomicInterval, index=0) -> Dict[str, Any]:
        # extract the locus fields
        d: Dict[str, Any] = {
            'chromosome': gene.locus.chromosome,
            'start' : gene.locus.interval.start + index,
            'end' : gene.locus.interval.end,
            'strand' : gene.locus.strand,
            'data' : gene.locus.data,
            'children' : [self._gene_to_dict(child, index) for child in gene.children]
        }
        return d