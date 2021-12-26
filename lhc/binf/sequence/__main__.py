import argparse

from .tools import barcode_filter, extract, filter, split, stat_, unique


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()
    for name, define_parser_ in (
        ('barcode_filter', barcode_filter.define_parser),
        ('extract', extract.define_parser),
        ('filter', filter.define_parser),
        ('split', split.define_parser),
        ('stat', stat_.define_parser),
        ('unique', unique.define_parser),
    ):
        subparser = subparsers.add_parser(name)
        define_parser_(subparser)
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
