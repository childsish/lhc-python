import argparse

from typing import Iterable, Iterator
from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.io.loci import open_loci_file
from lhc.itertools.merge_sorted import merge_sorted


def closest(loci: Iterable[GenomicInterval], query: Iterable[GenomicInterval]) -> Iterator[GenomicInterval]:
    previous = None
    unmatched = None
    for loci in merge_sorted(iter(loci), iter(query)):
        if len(loci[0]) > 0:
            if len(loci[1]) > 0:
                yield loci[0][0].data['gene_id'], loci[0][0], loci[1][0], 0
            else:
                unmatched = loci[0][0]
        if len(loci[1]) > 0:
            if unmatched:
                if previous:
                    if unmatched.start - previous.start < loci[1][0].start - unmatched.start:
                        yield unmatched.data['gene_id'], unmatched, previous, unmatched.start - previous.start
                    else:
                        yield unmatched.data['gene_id'], unmatched, loci[1][0], loci[1][0].start - unmatched.start
                else:
                    yield unmatched.data['gene_id'], unmatched, loci[1][0], loci[1][0].start - unmatched.start
                unmatched = None
            previous = loci[1][0]


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
    parser.set_defaults(func=init_closest)
    return parser


def init_closest(args):
    with open_loci_file(args.input, format=args.input_format, index=args.input_index) as input,\
            open_loci_file(args.output, 'w', format=args.output_format, index=args.output_index) as output,\
            open_loci_file(args.loci, format=args.loci_format, index=args.loci_index) as loci:
        for locus in closest(input, loci):
            print(locus)


if __name__ == '__main__':
    main()
