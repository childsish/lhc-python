import argparse
import sys

from lhc.io.sequence import Sequence, open_sequence_file


def call_variants(sequences):
    sequence_iterator = iter(sequences)
    reference = next(sequence_iterator)
    for sequence in sequence_iterator:
        call_variants_pairwise(reference, sequence)


def call_variants_pairwise(reference: Sequence, sequence: Sequence):
    print(reference)
    print(sequence)
    reference_position = 0
    start = None
    reference_start = None
    variant_type = None
    for index, (item1, item2) in enumerate(zip(reference, sequence)):
        reference_position += item1 != '-'
        if variant_type is None and item1 == item2:
            continue
        elif item1 == item2:
            print(reference_start, variant_type, reference[start:index], sequence[start:index])
            variant_type = None
            continue

        if item1 == '-':
            if variant_type != 'insertion':
                if variant_type:
                    print(reference_start, variant_type, reference[start:index], sequence[start:index])
                variant_type = 'insertion'
                start = index
                reference_start = reference_position
        elif item2 == '-':
            if variant_type != 'deletion':
                if variant_type:
                    print(reference_start, variant_type, reference[start:index], sequence[start:index])
                variant_type = 'deletion'
                start = index
                reference_start = reference_position
        elif variant_type != 'mismatch':
            if variant_type:
                print(reference_start, variant_type, reference[start:index], sequence[start:index])
            variant_type = 'mismatch'
            start = index
            reference_start = reference_position


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser())


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?')
    parser.set_defaults(func=init_call_variants)
    return parser


def init_call_variants(args):
    with open_sequence_file(args.input) as sequence_file:
        call_variants(sequence_file)


if __name__ == '__main__':
    sys.exit(main())
