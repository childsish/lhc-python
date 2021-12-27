import argparse

from .tools import barcode_filter, barcode_split, extract, filter, interleave, rmdup, split, stat_, unique, view


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()
    for module in [barcode_filter, barcode_split, extract, filter, interleave, rmdup, split, stat_, unique, view]:
        subparser = subparsers.add_parser(module.__name__)
        module.define_parser(subparser)
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
