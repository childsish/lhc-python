import argparse
import pysam

from typing import Iterable, Iterator
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.io.loci import open_loci_file


def query(loci: Iterable[GenomicInterval], query: pysam.TabixFile, direction: str = 'left') -> Iterator[GenomicInterval]:
    if direction == 'left':
        for locus in loci:
            if next(query.fetch(locus), None) is not None:
                yield locus
    elif direction == 'right':
        for locus in loci:
            for result in query.fetch(locus):
                yield result
    elif direction == 'diff':
        for locus in loci:
            if next(query.fetch(locus), None) is None:
                yield locus
    else:
        raise ValueError('Querying with unknown direction.')


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser())


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?',
                        help='input loci to filter (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='loci file to extract loci to (default: stdout).')
    parser.add_argument('-d', '--direction', default='left', choices=('left', 'right', 'diff'),
                        help='which loci to return')
    parser.add_argument('-l', '--loci', required=True,
                        help='loci to find intersections with')
    parser.add_argument('-i', '--input-format',
                        help='file format of input file (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format',
                        help='file format of output file (useful for writing to stdout).')
    parser.add_argument('--loci-format')
    parser.add_argument('--input-index', default=1, type=int)
    parser.add_argument('--output-index', default=1, type=int)
    parser.add_argument('--loci-index', default=1, type=int)
    parser.set_defaults(func=init_query)
    return parser


def init_query(args):
    with open_loci_file(args.input, format=args.input_format, index=args.input_index) as input,\
            open_loci_file(args.output, 'w', format=args.output_format, index=args.output_index) as output,\
            open_loci_file(args.loci, 'q', format=args.loci_format, index=args.loci_index) as loci:
        for locus in query(input, loci, args.direction):
            output.write(locus)


if __name__ == '__main__':
    main()
