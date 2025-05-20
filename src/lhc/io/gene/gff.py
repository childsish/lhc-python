from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .gene_file import GeneFile
from lhc.entities import NestedGenomicInterval, Locus, Interval
from lhc.io.parsers.gff import parse_gff

import json


@dataclass
class GeneLoci:
    loci: List[Locus] = field(default_factory=list)
    locus: Locus = None
    interval: Optional[Interval] = None


class GffFile(GeneFile):

    EXTENSION = ('.gff', '.gff.gz', '.gff3', '.gff3.gz')
    FORMAT = 'gff'
    
    def iter(self):
        genes: Dict[str, List[Tuple[Locus, ]]] = {}
        for line in self.file:
            if line.startswith('#'):
                continue
            locus = parse_gff(line)
            gene_id = locus.data['gene_id']
            
            if gene_id not in genes:
                genes[gene_id] = GeneLoci()
            genes[gene_id].loci.append(locus)
            
            if locus.data['feature'] == 'gene':
                genes[gene_id].locus = locus
                genes[gene_id].interval = locus.interval
            
            to_delete = []
            ready_loci = sorted((item for item in genes.items() if item[1].interval), key=lambda item: item[1].interval)
            for gene_id, gene_loci in ready_loci:
                if locus.interval.start <= gene_loci.interval.end:
                    break
            
                yield gene_loci.loci
                to_delete.append(gene_id)

            for gene_id in to_delete:
                del genes[gene_id]
                
        for gene_loci in sorted(genes.values(), key=lambda value: value.interval.start):
            if gene_loci.interval:
                yield gene_loci.loci
            

    def parse(self, loci: List[Locus]) -> NestedGenomicInterval:
        gene_locus = next(l for l in loci if l.data['feature']=='gene')
        gene = NestedGenomicInterval(
            chromosome=gene_locus.chromosome,
            interval=gene_locus.interval,
            strand=gene_locus.strand,
            data=gene_locus.data,
        )
        parents = {}

        for locus in loci:
            if locus.data['feature']=='transcript':
                transcript = NestedGenomicInterval(
                    chromosome=locus.chromosome,
                    interval=locus.interval,
                    strand=locus.strand,
                    data=locus.data,
                )
                gene.add_child(transcript)
                parents[transcript.locus.data['ID']] = transcript

        for locus in loci:
            if locus.data['feature'] not in ['gene', 'transcript']:
                parent = locus.data['Parent']
                exon = NestedGenomicInterval(
                    chromosome=locus.chromosome,
                    interval=locus.interval,
                    strand=locus.strand,
                    data=locus.data,
                )
                parents[parent].add_child(exon)
                parents[exon.locus.data['ID']] = exon

        return gene
    
    def format(self, gene: NestedGenomicInterval):
        lines = []
        attrs = {}
        for key in gene.locus.data:
            if key in {'source', 'feature', 'score', 'frame'}:
                continue
            value = gene.locus.data[key]
            if isinstance(value, list):
                value = ','.join(value)
            attrs[key] = value
        attrs = ';'.join('{}={}'.format(key, value) for key, value in attrs.items())
        lines.append(f'{gene.locus.chromosome}\t{gene.locus.data["source"]}\t{gene.locus.data["feature"]}\t{gene.locus.interval.start}\t{gene.locus.interval.end}\t{gene.locus.data["score"]}\t{gene.locus.strand}\t{gene.locus.data["frame"]}\t{attrs}')
        for transcript in gene.children:
            attrs = {}
            for key in transcript.locus.data:
                if key in {'source', 'feature', 'score', 'frame'}:
                    continue
                value = transcript.locus.data[key]
                if isinstance(value, list):
                    value = ','.join(value)
                attrs[key] = value
            attrs = ';'.join('{}={}'.format(key, value) for key, value in attrs.items())
            lines.append(f'{transcript.locus.chromosome}\t{transcript.locus.data["source"]}\t{transcript.locus.data["feature"]}\t{transcript.locus.interval.start}\t{transcript.locus.interval.end}\t{transcript.locus.data["score"]}\t{transcript.locus.strand}\t{transcript.locus.data["frame"]}\t{attrs}')
            for exon in transcript.children:
                attrs = {}
                for key in exon.locus.data:
                    if key in {'source', 'feature', 'score', 'frame'}:
                        continue
                    value = exon.locus.data[key]
                    if isinstance(value, list):
                        value = ','.join(value)
                    attrs[key] = value
                attrs = ';'.join('{}={}'.format(key, value) for key, value in attrs.items())
                lines.append(f'{exon.locus.chromosome}\t{exon.locus.data["source"]}\t{exon.locus.data["feature"]}\t{exon.locus.interval.start}\t{exon.locus.interval.end}\t{exon.locus.data["score"]}\t{exon.locus.strand}\t{exon.locus.data["frame"]}\t{attrs}')
        lines.append('')
        return '\n'.join(lines)
