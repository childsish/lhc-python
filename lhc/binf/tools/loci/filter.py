import gzip
import sys
import argparse

from contextlib import contextmanager
from typing import IO, Iterable, Optional
from lhc.binf.genomic_coordinate import GenomicInterval, open_iterator, get_formatter
from lhc.io.bed.iterator import BedLineIterator
from lhc.io.bed.formatter import BedFormatter
from lhc.io.gff.iterator import GffLineIterator
from lhc.io.gff.formatter import GffFormatter
from lhc.io.gtf.iterator import GtfLineIterator
from lhc.io.gtf.formatter import GtfFormatter


def filter(intervals: Iterable[GenomicInterval], expression=None) -> Iterable[GenomicInterval]:
    for interval in intervals:
        local_variables = {
            'chromosome': interval.chromosome,
            'start': interval.start,
            'stop': interval.stop,
            'strand': interval.strand
        }
        local_variables.update(interval.data)
        if eval(expression, local_variables):
            yield interval


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='?',
                        help='name of the intervals file to be filtered (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='name of the filtered intervals file (default: stdout).')
    parser.add_argument('-f', '--filter', required=True,
                        help='filter to apply (default: none).')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('-v', '--inverse', action='store_true',
                        help='invert filter.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--region',
                       help='apply filter in region (default: none).')
    group.add_argument('-x', '--exclude',
                       help='do not apply filter in region (default: none).')
    parser.set_defaults(func=init_filter)
    return parser


def init_filter(args):
    with open_iterator(args.input, args.input_format, [BedLineIterator, GffLineIterator, GtfLineIterator]) as input,\
            get_output(args.output) as output:
        formatter = get_formatter(args.output, args.output_format, [BedFormatter, GffFormatter, GtfFormatter])
        for item in input.hdr:
            output.write('{}\n'.format(item))
        for interval in filter(input, args.filter):
            output.write(formatter.format(interval))


@contextmanager
def get_output(filename: Optional[str]) -> IO:
    fileobj = sys.stdout if filename is None else \
        gzip.open(filename, 'wt', encoding='utf-8') if filename.endswith('.gz') else \
            open(filename, 'w', encoding='utf-8')
    yield fileobj
    fileobj.close()


if __name__ == '__main__':
    sys.exit(main())
