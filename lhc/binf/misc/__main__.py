import argparse

from .tools import cs_to_table


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()
    for name, define_parser in (
            ('cs_to_table', cs_to_table.define_parser),):
        subparser = subparsers.add_parser(name)
        define_parser(subparser)
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
