import string

from json import loads, dumps

from .locus_file import LocusFile
from lhc.entities.locus import Locus
from lhc.entities.interval import Interval


class JsonLFile(LocusFile):

    EXTENSION = ('.json', '.json.gz')
    FORMAT = 'jsonl'

    def iter(self):
        for line in self.file:
            data = loads(line)
            yield Locus(
                chromosome=data['chromosome'],
                interval=Interval(int(data['start']), int(data['end'])),
                strand=data['strand'],
                data=data['data'],
            )

    def format(self, locus: Locus, index=1) -> str:
        return dumps(
            {
                'start': locus.interval.start,
                'end': locus.interval.end,
                'chromosome': locus.chromosome,
                'strand': locus.strand,
                'data': locus.data,
            }
        )
