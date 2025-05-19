import string

from json import loads, dumps

from .locus_file import LocusFile
from lhc.entities.locus import Locus


class JsonLFile(LocusFile):

    EXTENSION = ('.json', '.json.gz')
    FORMAT = 'jsonl'

    def iter(self):
        for line in self.file:
            data = loads(line)
            yield Locus(
                int(data['start']),
                int(data['end']),
                chromosome=data['chromosome'],
                strand=data['strand'],
                data=data['data'],
            )

    def format(self, interval: Locus, index=1) -> str:
        return dumps(
            {
                'start': interval.start.position,
                'end': interval.end.position,
                'chromosome': interval.chromosome.chromosome,
                'strand': interval.strand,
                'data': interval.data,
            }
        )
