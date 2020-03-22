import argparse

from typing import Iterable, Iterator
from lhc.io.fasta.iterator import iter_fasta, FastaEntry
from lhc.io.file import open_file


def get_sequence_sizes(sequences: Iterable[FastaEntry]) -> Iterator[FastaEntry]:
    for sequence in sequences:
        yield len(sequence.seq)


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='*',
                        help='sequences to filter (default: stdin).')
    parser.add_argument('-o', '--output',
                        help='sequence file to filtered sequences to (default: stdout).')
    parser.set_defaults(func=init_stat)
    return parser


def init_stat(args: argparse.Namespace):
    with open_file(args.output, 'w') as output:
        for input in args.input:
            sequences = iter_fasta(input)
            for sequence in sequences:
                output.write('{}\t{}\n'.format(sequence.key, len(sequence.seq)))


if __name__ == '__main__':
    import sys
    sys.exit(main())
