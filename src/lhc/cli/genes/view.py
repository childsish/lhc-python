import sys
import argparse

from typing import Iterable, Iterator
from lhc.entities import NestedGenomicInterval
from lhc.io.gene import open_gene_file


def view(genes: Iterable[NestedGenomicInterval], major_transcript=False) -> Iterator[NestedGenomicInterval]:
    if not major_transcript:
        yield from genes
    else:
        for gene in genes:
            transcripts = []
            for transcript in gene.children:
                if not any(exon.locus.data['feature'] == 'CDS' for exon in transcript.children):
                    continue
                transcript_length = sum(exon.locus.interval.end - exon.locus.interval.start for exon in transcript.children if exon.locus.data['feature'] == 'exon')
                transcripts.append((transcript_length, transcript))
            
            if not transcripts:
                continue
            major_transcript = sorted(transcripts, key=lambda item: item[0])[-1][1]
            gene.children = [major_transcript]
            yield gene
    


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'View the genes in the given file'


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be viewed (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the output intervals file (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-m', '--major-transcript', action='store_true',
                        help='extract just the major transcript.')
    parser.set_defaults(func=init_view)
    return parser


def init_view(args):
    with open_gene_file(args.input, format=args.input_format) as input_,\
            open_gene_file(args.output, 'w', format=args.output_format) as output:
        for gene in view(input_, args.major_transcript):
            output.write(gene)


if __name__ == '__main__':
    sys.exit(main())
