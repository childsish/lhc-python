import sys
import argparse

from typing import Iterable, Iterator
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.io.loci import open_loci_file
from pysam import TabixFile


def shear(intervals: Iterable[GenomicInterval], shears: TabixFile) -> Iterator[GenomicInterval]:
    """
    Shear each interval in `intervals` using intervals from `shears`. Shearing truncates the interval downstream of the
    shear.
    :param intervals: intervals to shear
    :param shears: intervals to use as shears
    :return: shorn intervals
    """
    with open_loci_file(shears.filename.decode('utf-8')) as parser:
        for interval in intervals:
            try:
                overlapping = [parser.parse(locus) for locus in shears.fetch(interval.chromosome, interval.start.position, interval.stop.position) if 'exon' in locus and 'protein_coding' in locus]
                if overlapping:
                    if interval.strand == '+' and interval.data['feature'] == '5p_flank':
                        start = max(overlap.stop for overlap in overlapping if overlap.strand == interval.strand)
                        interval.start = start
                    elif interval.strand == '+' and interval.data['feature'] == '3p_flank':
                        stop = min(overlap.start for overlap in overlapping if overlap.strand == interval.strand)
                        interval.stop = stop
                    elif interval.strand == '-' and interval.data['feature'] == '5p_flank':
                        stop = min(overlap.start for overlap in overlapping if overlap.strand == interval.strand)
                        stop.strand = '-'
                        interval.stop = stop
                    else:
                        start = max(overlap.stop for overlap in overlapping if overlap.strand == interval.strand)
                        start.strand = '-'
                        interval.start = start
                if interval.stop > interval.start:
                    yield interval
            except ValueError:
                sys.stderr.write((str(interval) + '\n'))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be sheared (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the sheared intervals file (default: stdout).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-s', '--shears', required=True,
                        help='loci to shear input with')
    parser.set_defaults(func=init_shear)
    return parser


def init_shear(args):
    with open_loci_file(args.input, format=args.input_format) as input,\
            open_loci_file(args.output, 'w', format=args.output_format) as output:
        shears = TabixFile(args.shears)
        for interval in shear(input, shears):
            output.write(interval)


if __name__ == '__main__':
    sys.exit(main())
