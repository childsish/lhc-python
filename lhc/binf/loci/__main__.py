import argparse

from .tools import closest, filter, extend, query, view


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()

    closest_parser = subparsers.add_parser('closest')
    closest.define_parser(closest_parser)
    extend_parser = subparsers.add_parser('extend')
    extend.define_parser(extend_parser)
    filter_parser = subparsers.add_parser('filter')
    filter.define_parser(filter_parser)
    query_parser = subparsers.add_parser('query')
    query.define_parser(query_parser)
    view_parser = subparsers.add_parser('view')
    view.define_parser(view_parser)

    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
