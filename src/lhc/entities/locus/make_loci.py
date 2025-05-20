import heapq

from typing import Dict, Iterable, Iterator, List
from lhc.entities.locus import Locus, NestedGenomicInterval


def make_loci(loci: Iterable[Locus], *, tolerance: int = 100000) -> Iterator[NestedGenomicInterval]:
    tops = []  # type: List[NestedGenomicInterval]
    parents = {}  # type: Dict[str, NestedGenomicInterval]
    for locus in loci:
        gene_id = locus.data['gene_id'][0]
        transcript_id = locus.data['transcript_id'][0] if 'transcript_id' in locus.data else locus.data['gene_id'][0] + '.1'
        nested_locus = NestedGenomicInterval(locus.chromosome, locus.interval, locus.strand, locus.data)

        if 'feature' not in locus.data or locus.data['feature'] == 'gene':
            heapq.heappush(tops, nested_locus)
            parents[gene_id] = nested_locus
        elif locus.data['feature'] == 'transcript':
            parents[transcript_id] = nested_locus
            parents[gene_id].add_child(nested_locus)
        else:
            if gene_id not in parents:
                top = NestedGenomicInterval(locus.chromosome, locus.interval, locus.strand, locus.data)
                heapq.heappush(tops, top)
                parents[gene_id] = top
            if transcript_id not in parents:
                parents[transcript_id] = NestedGenomicInterval(locus.chromosome, locus.interval, locus.strand, locus.data)
                parents[gene_id].add_child(parents[transcript_id])
            parents[transcript_id].add_child(nested_locus)

        while len(tops) > 0 and tops[0].locus.data['gene_id'] != gene_id and tops[0].locus.interval.end + tolerance < locus.interval.start:
            gene = tops.pop(0)
            for transcript in gene.children:
                transcript_id = transcript.locus.data['transcript_id'][0]
                if transcript_id in parents:
                    del parents[transcript_id]
            gene_id = gene.locus.data['gene_id'][0]
            if gene_id in parents:
                del parents[gene_id]
            yield gene

    yield from tops
