import argparse
import pysam

from textwrap import TextWrapper
from typing import Generator, Iterable, Set
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.binf.sequence.reverse_complement import reverse_complement
from lhc.io.loci import open_loci_file
from lhc.io.file import open_file


def extract(loci: Iterable[GenomicInterval], sequences: pysam.FastaFile) -> Generator[str, None, Set[str]]:
    missing_chromosomes = set()
    for locus in loci:
        identifier = str(locus.chromosome)

        if identifier not in sequences.references:
            missing_chromosomes.add(identifier)
            continue

        sequence = sequences.fetch(identifier, locus.start.position, locus.stop.position)
        yield reverse_complement(sequence) if locus.strand == '-' else sequence
    print('\n'.join(sorted(missing_chromosomes)))
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
    parser.add_argument('-f', '--format', default='{gene_id}',
                        help='format string to use as the header of the fasta entry.')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-s', '--sequence', required=True,
                        help='sequence file to extract loci from')
    parser.set_defaults(func=init_extract)
    return parser


def init_extract(args):
    wrapper = TextWrapper()
    with open_loci_file(args.input) as loci, open_file(args.output, 'w') as output:
        sequences = pysam.FastaFile(args.sequence)
        for locus, sequence in zip(loci, extract(loci, sequences)):
            output.write('>{}\n{}\n'.format(locus.data['gene_id'], '\n'.join(wrapper.wrap(sequence))))


if __name__ == '__main__':
    import sys
    sys.exit(main())
