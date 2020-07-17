import sys
import argparse

from typing import Iterable, Iterator
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.io.loci import open_loci_file


def flank(intervals: Iterable[GenomicInterval], *, five_prime=0, three_prime=0) -> Iterator[GenomicInterval]:
    """
    Create flanking intervals for each interval in `intervals`.
    :param intervals: intervals to flank
    :param five_prime: how much upstream to flank
    :param three_prime: how much downstream to flank
    :return: tuple of five- and three-prime flanks
    """
    for interval in intervals:
        five_prime_interval = None if five_prime == 0 else \
            GenomicInterval(interval.start - five_prime, interval.start, chromosome=interval.chromosome,
                            strand=interval.strand, data=interval.data) if interval.strand == '+' else \
            GenomicInterval(interval.stop, interval.stop + three_prime, chromosome=interval.chromosome,
                            strand=interval.strand, data=interval.data)
        three_prime_interval = None if three_prime == 0 else \
            GenomicInterval(interval.stop, interval.stop + five_prime, chromosome=interval.chromosome,
                            strand=interval.strand, data=interval.data) if interval.strand == '+' else \
            GenomicInterval(interval.start - three_prime, interval.start, chromosome=interval.chromosome,
                            strand=interval.strand, data=interval.data)
        yield five_prime_interval, three_prime_interval


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be flanked (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the flanked intervals file (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-5', '--five-prime', type=int, default=0,
                        help='flank in the 5\' direction.')
    parser.add_argument('-3', '--three-prime', type=int, default=0,
                        help='flank in the 3\' direction.')
    parser.set_defaults(func=init_flank)
    return parser


def init_flank(args):
    if not (args.five_prime or args.three_prime):
        raise ValueError('At least one of --five-prime or --three-prime must be specified.')
    with open_loci_file(args.input, format=args.input_format) as input,\
            open_loci_file(args.output, 'w', format=args.output_format) as output:
        for five_prime, three_prime in flank(input, five_prime=args.five_prime, three_prime=args.three_prime):
            if five_prime is not None:
                output.write(five_prime)
            if three_prime is not None:
                output.write(three_prime)


if __name__ == '__main__':
    sys.exit(main())
