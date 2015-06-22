__author__ = 'Liam Childs'

import argparse

from .vcf_ import merger
from .vcf_.iterator import VcfEntryIterator
from .vcf_.tools import compare, filter, sample, split_alt, trim_alt
from .txt_.tools import compress


def iter_vcf(fname):
    return VcfEntryIterator(fname)


def main():
    parser = get_parser()
    args = parser.parse_args()
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
    # Merge parser
    merge_parser = subparsers.add_parser('merge')
    merger.define_parser(merge_parser)
    # Filter parser
    filter_parser = subparsers.add_parser('filter')
    filter.define_parser(filter_parser)
    # Sample parser
    sample_parser = subparsers.add_parser('sample')
    sample.define_parser(sample_parser)
    # SplitAlt parser
    split_alt_parser = subparsers.add_parser('split_alt')
    split_alt.define_parser(split_alt_parser)
    # TrimAlt parser
    trim_alt_parser = subparsers.add_parser('trim_alt')
    trim_alt.define_parser(trim_alt_parser)
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
