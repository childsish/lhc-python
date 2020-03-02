import argparse
import pysam

from textwrap import TextWrapper
from typing import Generator, Iterable, Optional, Set
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.binf.sequence.reverse_complement import reverse_complement
from lhc.io.loci import open_loci_file
from lhc.io.file import open_file


def extract(regions: Iterable[GenomicInterval], sequences: pysam.FastaFile, extract_by_id: Optional[str] = None) -> Generator[str, None, Set[str]]:
    missing_chromosomes = set()
    for region in regions:
        identifier = format_region(extract_by_id, region) if extract_by_id else str(region.chromosome)

        if identifier not in sequences.references:
            missing_chromosomes.add(identifier)
            continue

        sequence = sequences.fetch(identifier) if extract_by_id else \
            sequences.fetch(identifier, region.start.position, region.stop.position)
        yield reverse_complement(sequence) if region.strand == '-' else sequence
    print('\n'.join(sorted(missing_chromosomes)))
    return missing_chromosomes


def format_region(format_string: str, region: GenomicInterval) -> str:
    return format_string.format(chromosome=region.chromosome,
                                start=region.start.position,
                                end=region.stop.position,
                                strand=region.strand,
                                **region.data)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='regions to extract (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='sequence file to extract sequences to (default: stdout).')
    parser.add_argument('-b', '--by',
                        help='if defined, use this format string to query the sequences.')
    parser.add_argument('-f', '--format', default='{gene_id}',
                        help='format string to use as the header of the fasta entry.')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-s', '--sequence', required=True,
                        help='sequence file to extract regions from')
    parser.set_defaults(func=init_extract)
    return parser


def init_extract(args):
    wrapper = TextWrapper()
    with open_loci_file(args.input) as regions, open_file(args.output, 'w') as output:
        sequences = pysam.FastaFile(args.sequence)
        for region, sequence in zip(regions, extract(regions, sequences, args.by)):
            output.write('>{}\n{}\n'.format(region.data['gene_id'], '\n'.join(wrapper.wrap(sequence))))


if __name__ == '__main__':
    import sys
    sys.exit(main())
