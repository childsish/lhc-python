import argparse

from lhc.binf.variant.tools import annotate, compare, diff, filter, merge, sample, shift


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()

    annotate_parser = subparsers.add_parser('annotate')
    annotate.define_parser(annotate_parser)

    compare_parser = subparsers.add_parser('compare')
    compare.define_parser(compare_parser)

    diff_parser = subparsers.add_parser('diff')
    diff.define_parser(diff_parser)

    filter_parser = subparsers.add_parser('filter')
    filter.define_parser(filter_parser)

    merge_parser = subparsers.add_parser('merge')
    merge.define_parser(merge_parser)

    sample_parser = subparsers.add_parser('sample')
    sample.define_parser(sample_parser)

    shift_parser = subparsers.add_parser('shift')
    shift.define_parser(shift_parser)

    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
