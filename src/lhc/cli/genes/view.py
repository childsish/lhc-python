import sys
import argparse

from typing import Iterable, Iterator
from lhc.entities.locus import Locus
from lhc.entities.locus.make_loci import make_loci
from lhc.io.gene import open_gene_file


def view(intervals: Iterable[Gene]) -> Iterator[Gene]:
    yield from intervals


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
    parser.add_argument('-o', '--output-format', default='jsonl',
                        help='file format of output file (useful for writing to stdout).')
    parser.set_defaults(func=init_view)
    return parser


def init_view(args):
    with open_gene_file(args.input, format=args.input_format) as input_,\
            open_gene_file(args.output, 'w', format=args.output_format) as output:
        for gene in view(input_):
            output.write(gene)


if __name__ == '__main__':
    sys.exit(main())
