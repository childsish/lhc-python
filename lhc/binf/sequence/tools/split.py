import argparse
import os
import re

from functools import partial
from textwrap import TextWrapper
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Tuple
from lhc.io.fasta.iterator import iter_fasta, FastaEntry
from lhc.filetools.filepool import FilePool


def split(sequences: Iterable[FastaEntry], mappers: List[Callable], *, unmapped='discard') -> Iterator[Tuple[str, FastaEntry]]:
    def map_to_filename(sequence_: FastaEntry) -> str:
        for mapper in mappers:
            filename_ = mapper(sequence_)
            if filename_:
                return filename_
        return None if unmapped == 'discard' else\
            'unmapped' if unmapped == 'join' else\
            sequence.key

    for sequence in sequences:
        if len(sequence.seq) == 0:
            continue
        filename = map_to_filename(sequence)
        if filename:
            yield filename, sequence


def map_by_map(sequence: FastaEntry, map_: Dict[str, str]) -> Optional[str]:
    return map_.get(sequence.key, None)


def map_by_regx(sequence: FastaEntry, regx: re.Pattern, replacement: str, description=False) -> Optional[str]:
    match = regx.match(sequence.key)
    if match:
        return regx.sub(replacement, sequence.key)
    elif description:
        match = regx.match(sequence.hdr)
        if match:
            return regx.sub(replacement, sequence.hdr)
    return None


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.add_argument('input', nargs='*',
                        help='sequences to filter (default: stdin).')
    parser.add_argument('-d', '--description', action='store_true',
                        help='search also in description field.')
    parser.add_argument('-o', '--output',
                        help='directory for output files')
    parser.add_argument('-r', '--regular-expression', nargs=2,
                        help='split using regular expression')
    parser.add_argument('-m', '--map',
                        help='split using a map')
    parser.add_argument('-u', '--unmapped', choices=['discard', 'keep', 'split'], default='split',
                        help='whether the unmapped sequences should be discarded, output to a single file or output to multiple files')
    parser.set_defaults(func=init_split)
    return parser


def init_split(args: argparse.Namespace):
    wrapper = TextWrapper()
    mappers = []

    outputs = FilePool(mode='w')
    if args.map:
        with open(args.map) as fileobj:
            mappers.append(partial(map_by_map, map_=dict(line.strip().split() for line in fileobj)))
    if args.regular_expression:
        mappers.append(partial(map_by_regx, regx=re.compile(args.regular_expression[0]), replacement=args.regular_expression[1], description=args.description))

    sequence_iterators = [('stdin', iter_fasta(sys.stdin))] if args.input is None else ((input, iter_fasta(input)) for input in args.input if input)
    for input, sequences in sequence_iterators:
        for filename, sequence in split(sequences, mappers, unmapped=args.unmapped):
            outputs[os.path.join(args.output, '{}.fasta'.format(filename))].write('>{} "{}"\n{}\n'.format(sequence.hdr, input, '\n'.join(wrapper.wrap(sequence.seq.replace('-', '')))))


if __name__ == '__main__':
    import sys
    sys.exit(main())
