import argparse
import pysam
import sys

from itertools import tee
from textwrap import TextWrapper
from typing import Generator, Iterable, Set
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.binf.loci.make_loci import make_loci
from lhc.binf.sequence.reverse_complement import reverse_complement
from lhc.io.loci import open_loci_file
from lhc.io.file import open_file


def extract(loci: Iterable[GenomicInterval], sequences: pysam.FastaFile, stranded=True) -> Generator[str, None, Set[str]]:
    missing_chromosomes = set()
    for locus in loci:
        if str(locus.chromosome) not in sequences.references:
            missing_chromosomes.add(str(locus.chromosome))
            continue
        sequence = sequences.fetch(str(locus.chromosome), locus.start.position, locus.stop.position)
        yield reverse_complement(sequence) if locus.strand == '-' and stranded else sequence
    sys.stderr.write('\n'.join(sorted(missing_chromosomes)))
    return missing_chromosomes


def format_locus(format_string: str, locus: GenomicInterval) -> str:
    return format_string.format(chromosome=locus.chromosome,
                                start=locus.start.position,
                                end=locus.stop.position,
                                strand=locus.strand,
                                **locus.data)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='loci to extract (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='sequence file to extract sequences to (default: stdout).')
    parser.add_argument('-a', '--assemble', action='store_true',
                        help='assemble loci models before extracting sequences')
    parser.add_argument('-f', '--format', default='{gene_id}',
                        help='format string to use as the header of the fasta entry.')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-s', '--sequence', required=True,
                        help='sequence file to extract loci from')
    parser.add_argument('-u', '--unstranded', action='store_false',
                        help='whether to keep the strand of the locus (default: true)')
    parser.set_defaults(func=init_extract)
    return parser


def init_extract(args):
    wrapper = TextWrapper()
    with open_loci_file(args.input, format=args.input_format) as loci, open_file(args.output, 'w') as output:
        sequences = pysam.FastaFile(args.sequence)
        if args.assemble:
            loci = make_loci(loci)
        left, right = tee(loci)
        for locus, sequence in zip(left, extract(right, sequences, args.unstranded)):
            output.write('>{}\n{}\n'.format(locus.data['gene_id'], '\n'.join(wrapper.wrap(sequence))))


if __name__ == '__main__':
    sys.exit(main())
