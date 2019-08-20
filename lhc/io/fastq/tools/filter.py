import argparse

from lhc.io.fastq import iter_fastq
from lhc.misc.string import hamming


def filter(read_files, filters):
    input_streams = [iter_fastq(open(read_file) for read_file in read_files)]
    output_streams = [open('{}.filtered.fastq'.format(read_file), 'w') for read_file in read_files]
    for reads in zip(input_streams):
        if all(hamming(reads[index], sequence) < mismatches for sequence, mismatches, index in filters):
            for read, output_stream in zip(reads, output_streams):
                output_stream.write(str(read))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser())


def define_parser(parser) -> argparse.ArgumentParser:
    parser.add_argument('read_files', nargs='+')
    parser.add_argument('-f', '--filter', dest='filters', nargs=3, action='append')
    parser.set_defaults(func=filter)
    return parser


def init_filter(args):
    filters = [(sequence, int(mismatches), int(index)) for sequence, mismatches, index in args.filters]
    filter(args.read_files, filters)


if __name__ == '__main__':
    import sys
    sys.exit(main())
