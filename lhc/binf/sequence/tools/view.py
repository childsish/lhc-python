import argparse

from textwrap import TextWrapper
from typing import Iterable, Iterator
from lhc.io import open_file
from lhc.io.fasta.iterator import iter_fasta, FastaEntry


def view(sequences: Iterable[FastaEntry]) -> Iterator[FastaEntry]:
    for sequence in sequences:
        yield FastaEntry(sequence.key, sequence.hdr, sequence.seq.replace('-', ''))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser())


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?',
                        help='sequences to view (default: stdin).')
    parser.add_argument('output', nargs='?',
                        help='sequence file to write viewed sequences to (default: stdout).')
    parser.set_defaults(func=init_view)
    return parser


def init_view(args: argparse.Namespace):
    wrapper = TextWrapper()
    with open_file(args.input) as input, open_file(args.output, 'w') as output:
        sequences = iter_fasta(input)
        for sequence in view(sequences):
            output.write('>{}\n{}\n'.format(sequence.hdr, '\n'.join(wrapper.wrap(sequence.seq))))


if __name__ == '__main__':
    import sys
    sys.exit(main())
