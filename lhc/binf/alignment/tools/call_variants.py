import argparse
import sys

from lhc.binf.variant import CodingVariant, CodonVariant, Variant
from lhc.io.sequence import Sequence, open_sequence_file
from lhc.io.locus import open_locus_file


def call_variants(sequences, loci=None):
    sequence_iterator = iter(sequences)
    reference = next(sequence_iterator)
    for sequence in sequence_iterator:
        call_variants_pairwise(reference, sequence, loci)
    print(loci)


def call_variants_pairwise(reference: Sequence, sequence: Sequence, loci=None):
    nucleotide_variants = call_nucleotide_variants(reference, sequence)
    coding_variants = [None] * len(nucleotide_variants)
    codon_variants = [None] * len(nucleotide_variants)
    if loci is not None:
        reference_sequence = reference.sequence.replace('-', '')
        coding_variants = call_coding_variants(nucleotide_variants, loci)
        codon_variants = call_codon_variants(coding_variants, {locus.data['/product']: reference_sequence[locus.start.position:locus.stop.position] for locus in loci})
    for nucleotide_variant, coding_variant, codon_variant in zip(nucleotide_variants, coding_variants, codon_variants):
        print(nucleotide_variant, coding_variant, codon_variant)
    print()
    return nucleotide_variants, coding_variants


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
        Variant(reference_start, reference_alignment[start:stop], alternate_alignment[start:stop])


def call_coding_variants(nucleotide_variants, loci):
    assert all(loci[i] < loci[i + 1] for i in range(len(loci) - 1))

    nucleotide_variant_iterator = iter(nucleotide_variants)
    locus_iterator = iter(loci)
    nucleotide_variant = next(nucleotide_variant_iterator)
    locus = next(locus_iterator)

    coding_variants = []
    while nucleotide_variant is not None and locus is not None:
        if nucleotide_variant.pos < locus.start:
            coding_variants.append(None)
            nucleotide_variant = next(nucleotide_variant_iterator, None)
        elif nucleotide_variant.pos >= locus.stop:
            locus = next(locus_iterator, None)
        else:
            coding_position = locus.get_rel_pos(nucleotide_variant.pos)
            coding_variants.append(CodingVariant(locus.data['/product'], coding_position, nucleotide_variant.ref, nucleotide_variant.alt))
            nucleotide_variant = next(nucleotide_variant_iterator, None)

    while nucleotide_variant is not None:
        coding_variants.append(None)
        nucleotide_variant = next(nucleotide_variant_iterator, None)

    return coding_variants


def call_codon_variants(coding_variants, reference_sequences):
    codon_variants = []
    for variant in coding_variants:
        if variant is None:
            codon_variants.append(None)
            continue

        reference_sequence = reference_sequences[variant.id]
        assert reference_sequence[variant.pos:variant.pos + len(variant.ref)] == variant.ref

        if len(variant.ref) == 1:
            fr = variant.pos % 3
            to = 2 - (variant.pos % 3)
        else:
            fr = [3, 4, 2][variant.pos % 3]
            to = [2, 4, 3][(variant.pos + len(variant.ref) )% 3]
        sequence = list(reference_sequence)
        sequence[variant.pos:variant.pos + len(variant.ref)] = list(variant.alt)

        d = len(variant.ref) - len(variant.alt)
        fs_pos = None
        if d != 0:
            fs_pos = 0
            sequence = reference_sequence[variant.pos + 1:]
            while fs_pos < len(sequence) and sequence[fs_pos:fs_pos + 3] not in {'TAA', 'TAG', 'TGA'}:
                fs_pos += 3
        ref_codon = ''.join(reference_sequence[variant.pos - fr:variant.pos + len(variant.ref) + to])
        codon_variants.append(CodonVariant(variant.pos - fr, ref_codon, ''.join(sequence[variant.pos - fr: variant.pos + len(variant.alt) + to]), fs_pos))
    return codon_variants


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
        call_variants(sequence_file, loci)


if __name__ == '__main__':
    sys.exit(main())
