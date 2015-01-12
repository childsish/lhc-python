import argparse
import sys

from vcf_.iterator import VcfEntryIterator, VcfLineIterator
from vcf_ import merger, sample, filter


def iter_entries(fname):
    return VcfEntryIterator(fname)


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    merge_parser = subparsers.add_parser('merge')
    merger.define_parser(merge_parser)

    filter_parser = subparsers.add_parser('filter')
    filter.define_parser(filter_parser)

    sample_parser = subparsers.add_parser('sample')
    sample.define_parser(sample_parser)

    return parser


if __name__ == '__main__':
    sys.exit(main())
