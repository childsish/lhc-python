import argparse

from lhc.io.variant import open_variant_file, VariantFile
from lhc.io.txt import Filter


def compare(a: VariantFile, b: VariantFile, filter_=None):
    if filter_ is not None:
        a = Filter(a, filter_, {'NOCALL': 'NOCALL', 'PASS': 'PASS'})
        b = Filter(b, filter_, {'NOCALL': 'NOCALL', 'PASS': 'PASS'})
    set_a = set((line.chr, line.pos, line.ref, line.alt) for line in a)
    set_b = set((line.chr, line.pos, line.ref, line.alt) for line in b)
    sys.stdout.write('{}\t{}\t{}'.format(len(set_a - set_b), len(set_b - set_a), len(set_a & set_b)))


def main():
    args = get_parser().parse_args()
    args.func(args)

    
def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    add_arg = parser.add_argument
    add_arg('a')
    add_arg('b')
    add_arg('-f', '--filter',
            help='filter for variants (default: none).')
    parser.set_defaults(func=init_compare)
    return parser


def init_compare(args):
    with open_variant_file(args.a, encoding='utf-8') as a, \
            open_variant_file(args.b, encoding='utf-8') as b:
        compare(a, b, args.filter)


if __name__ == '__main__':
    import sys
    sys.exit(main())
