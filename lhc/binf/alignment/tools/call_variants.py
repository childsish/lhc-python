import argparse
import sys

from lhc.binf.variant import call_amino_acid_variants, call_coding_variants, call_codon_variants, call_variant_effects, Variant
from lhc.io.sequence import Sequence, open_sequence_file
from lhc.io.locus import open_locus_file


def call_variants(sequences, loci=None):
    sequence_iterator = iter(sequences)
    reference = next(sequence_iterator)
    for sequence in sequence_iterator:
        for variants in call_variants_pairwise(reference, sequence, loci):
            yield sequence.identifier, variants


def call_variants_pairwise(reference: Sequence, sequence: Sequence, loci=None):
    nucleotide_variants = call_nucleotide_variants(reference, sequence)
    coding_variants = [None] * len(nucleotide_variants)
    codon_variants = [None] * len(nucleotide_variants)
    amino_acid_variants = [None] * len(nucleotide_variants)
    variant_effects = [None] * len(nucleotide_variants)
    if loci is not None:
        reference_sequence = reference.sequence.replace('-', '')
        coding_variants = call_coding_variants(nucleotide_variants, loci)
        codon_variants = call_codon_variants(coding_variants, {locus.data['product']: reference_sequence[locus.start.position:locus.stop.position + 3] for locus in loci})
        amino_acid_variants = call_amino_acid_variants(codon_variants)
        variant_effects = call_variant_effects(amino_acid_variants)
    yield from zip(nucleotide_variants, coding_variants, codon_variants, amino_acid_variants, variant_effects)


def call_nucleotide_variants(reference: Sequence, sequence: Sequence):
    reference_sequence = reference.sequence.replace('-', '')
    variants = []
    reference_position = -1
    start = None
    reference_start = None
    variant_type = None
    iterator = enumerate(zip(reference, sequence))
    for index, (item1, item2) in iterator:
        reference_position += item1 != '-'
        if variant_type is None and item1 == item2 or item1 == '-' and item2 == '-':
            continue
        elif item1 == item2:
            variants.append(get_nucleotide_variant(variant_type, reference_start, reference, sequence, start, index, reference_sequence))
            variant_type = None
            continue

        if item1 == '-':
            if variant_type != 'insertion':
                if variant_type:
                    variants.append(get_nucleotide_variant(variant_type, reference_start, reference, sequence, start, index, reference_sequence))
                variant_type = 'insertion'
                start = index
                reference_start = reference_position
        elif item2 == '-':
            if variant_type != 'deletion':
                if variant_type:
                    variants.append(get_nucleotide_variant(variant_type, reference_start, reference, sequence, start, index, reference_sequence))
                variant_type = 'deletion'
                start = index
                reference_start = reference_position
        elif variant_type != 'mismatch':
            if variant_type:
                variants.append(get_nucleotide_variant(variant_type, reference_start, reference, sequence, start, index, reference_sequence))
            variant_type = 'mismatch'
            start = index
            reference_start = reference_position
    if variant_type is not None:
        variants.append(get_nucleotide_variant(variant_type, reference_start, reference, sequence, start, len(reference), reference_sequence))
    return variants


def get_nucleotide_variant(variant_type, reference_start, reference_alignment, alternate_alignment, start, stop, reference_sequence):
    lead = None if reference_start == 0 else reference_sequence[reference_start - 1]
    return Variant(reference_start + 1, '', alternate_alignment[start: stop].replace('-', ''), lead=lead) if variant_type == 'insertion' else\
        Variant(reference_start, reference_alignment[start:stop].replace('-', ''), '', lead=lead) if variant_type == 'deletion' else\
        Variant(reference_start, reference_alignment[start:stop].replace('-', ''), alternate_alignment[start:stop].replace('-', ''))


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser() -> argparse.ArgumentParser:
    return define_parser(argparse.ArgumentParser())


def define_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('input', nargs='?')
    parser.add_argument('-l', '--loci')
    parser.set_defaults(func=init_call_variants)
    return parser


def init_call_variants(args):
    with open_sequence_file(args.input) as sequence_file:
        loci = None
        if args.loci is not None:
            with open_locus_file(args.loci) as locus_file:
                loci = list(locus_file)
        for id, variants in call_variants(sequence_file, loci):
            sys.stdout.write('{}\t{}\n'.format(id, '\t'.join(str(variant) for variant in variants)))


if __name__ == '__main__':
    sys.exit(main())
