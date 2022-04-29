import argparse

from lhc.io.locus import open_locus_file
from lhc.entities.interval.set_operations import set_intersect


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser(description=get_description()))


def get_description() -> str:
    return 'get the intersecting loci between two sets'


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('a', nargs='?',
                        help='input loci to intersect (default: stdin).')
    parser.add_argument('b',
                        help='input loci to intersect.')
    parser.add_argument('-r', '--result', default='b', choices=('a', 'b', 'ab'),
                        help='a - return loci from set a. b - return loci from set b. ab - intersection of the loci')
    parser.add_argument('-i', '--input-format',
                        help='file format of set a loci (useful for reading from stdin).')
    parser.add_argument('-o', '--output-format', default='bed',
                        help='file format of output file (useful for writing to stdout).')
    parser.set_defaults(func=init_intersect)
    return parser


def init_intersect(args):
    with open_locus_file(args.a, format=args.input_format) as left,\
        open_locus_file(args.b) as right,\
        open_locus_file(mode='w') as output\
    :
        intersecting_loci = set_intersect(left, right) if args.r == 'a' else\
            set_intersect(right, left) if args.r == 'b' else\
            set_intersect(left, right, intersect_intervals=True)
        for locus in intersecting_loci:
            output.write(locus)


if __name__ == '__main__':
    main()
