import string

from json import loads, dumps

from .locus_file import LocusFile
from lhc.entities.genomic_coordinate import GenomicInterval


class JsonLFile(LocusFile):

    EXTENSION = ('.json', '.json.gz')
    FORMAT = 'jsonl'

    def iter(self):
        for line in self.file:
            data = loads(line)
            yield GenomicInterval(
                int(data['start']),
                int(data['end']),
                chromosome=data['chromosome'],
                strand=data['strand'],
                data=data['data'],
            )

    def format(self, interval: GenomicInterval, index=1) -> str:
        return dumps(
            {
                'start': interval.start.position,
                'end': interval.end.position,
                'chromosome': interval.chromosome.chromosome,
                'strand': interval.strand,
                'data': interval.data,
            }
        )
