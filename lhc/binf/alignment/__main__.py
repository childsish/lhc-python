import argparse

from .tools import strand, mismatch_filter


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()

    strand_parser = subparsers.add_parser('strand')
    strand.define_parser(strand_parser)

    mismatch_filter_parser = subparsers.add_parser('mismatch_filter')
    mismatch_filter.define_parser(mismatch_filter_parser)

    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
