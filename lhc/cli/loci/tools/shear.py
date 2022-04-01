import argparse
import sys
import pysam

from typing import Iterable, Iterator
from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.io.locus import open_locus_file


def shear(intervals: Iterable[GenomicInterval], shears: pysam.TabixFile, stranded: False) -> Iterator[GenomicInterval]:
    """
    Shear each interval in `intervals` using intervals from `shears`. Shearing truncates the interval downstream of the
    shear.
    :param intervals: intervals to shear
    :param shears: intervals to use as shears
    :return: shorn intervals
    """
    with open_locus_file(shears.filename.decode('utf-8')) as parser:
        for interval in intervals:
            try:
                overlapping = [parser.parse(locus) for locus in shears.fetch(interval.chromosome, interval.start.position, interval.stop.position) if 'exon' in locus and 'protein_coding' in locus]
                if stranded:
                    overlapping = [locus for locus in overlapping if locus.strand == interval.strand]
                if overlapping:
                    if interval.strand == '-':
                        if interval.data['feature'] == '3p_flank':
                            start = max(overlap.stop for overlap in overlapping if overlap.strand == interval.strand)
                            start.strand = '-'
                            interval.start = start
                        else:
                            stop = min(overlap.start for overlap in overlapping if overlap.strand == interval.strand)
                            stop.strand = '-'
                            interval.stop = stop
                    else:
                        if interval.data['feature'] == '3p_flank':
                            stop = min(overlap.start for overlap in overlapping if overlap.strand == interval.strand)
                            interval.stop = stop
                        else:
                            start = max(overlap.stop for overlap in overlapping if overlap.strand == interval.strand)
                            interval.start = start
                if interval.stop > interval.start:
                    yield interval
            except ValueError:
                sys.stderr.write((str(interval) + '\n'))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'Remove parts of the loci that intersect with the given set of loci'


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
    parser.add_argument('--stranded', action='store_true',
                        help='whether to shear loci on both strands or just the same orientation')
    parser.set_defaults(func=init_shear)
    return parser


def init_shear(args):
    with open_locus_file(args.input, format=args.input_format) as input,\
            open_locus_file(args.output, 'w', format=args.output_format) as output:
        shears = pysam.TabixFile(args.shears)
        for interval in shear(input, shears, args.stranded):
            output.write(interval)


if __name__ == '__main__':
    sys.exit(main())
