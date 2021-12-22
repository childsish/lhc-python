import argparse

from lhc.binf.variant.tools import compare, diff, merge, sample, shift, split_alt, trim_alt
from lhc.io.txt.tools import sort, compress, index


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # Compare parser
    compare_parser = subparsers.add_parser('compare')
    compare.define_parser(compare_parser)
    # Compress parser
    compress_parser = subparsers.add_parser('compress')
    compress.define_parser(compress_parser)
    compress_parser.set_defaults(block_delimiter='\n')
    # Difference parser
    difference_parser = subparsers.add_parser('difference')
    diff.define_parser(difference_parser)
    # Sort parser
    sort_parser = subparsers.add_parser('sort')
    sort.define_parser(sort_parser)
    sort_parser.set_defaults(format='s1.i2')
    # Index parser
    index_parser = subparsers.add_parser('index')
    index.define_parser(index_parser)
    index_parser.set_defaults(format='s1.i2')
    # Merge parser
    merge_parser = subparsers.add_parser('merge')
    merge.define_parser(merge_parser)
    # Sample parser
    sample_parser = subparsers.add_parser('sample')
    sample.define_parser(sample_parser)
    # SplitAlt parser
    split_alt_parser = subparsers.add_parser('split_alt')
    split_alt.define_parser(split_alt_parser)
    # TrimAlt parser
    trim_alt_parser = subparsers.add_parser('trim_alt')
    trim_alt.define_parser(trim_alt_parser)
    # Shift parser
    shift_parser = subparsers.add_parser('shift')
    shift.define_parser(shift_parser)
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
