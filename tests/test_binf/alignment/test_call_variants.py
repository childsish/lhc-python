import unittest

from lhc.binf.alignment.tools.call_variants import call_nucleotide_variants, call_coding_variants, call_codon_variants, call_amino_acid_variants
from lhc.binf.genomic_coordinate import NestedGenomicInterval
from lhc.binf.variant import CodonVariant, CodingVariant, Variant
from lhc.io.sequence import Sequence


class TestCallVariants(unittest.TestCase):
    def test_call_nucleotide_variants_mismatch(self):
        reference_alignment = Sequence('ref', 'atatatta-ata-tat-')
        alternate_alignment = Sequence('alt', 'acacacca-aca-cac-')
        variants = call_nucleotide_variants(reference_alignment, alternate_alignment)

        self.assertEqual(6, len(variants))
        self.assertEqual(1, variants[0].pos)
        self.assertEqual(3, variants[1].pos)
        self.assertEqual(5, variants[2].pos)
        self.assertEqual(9, variants[3].pos)
        self.assertEqual(11, variants[4].pos)
        self.assertEqual(13, variants[5].pos)
        self.assertEqual('t', variants[0].ref)
        self.assertEqual('t', variants[1].ref)
        self.assertEqual('tt', variants[2].ref)
        self.assertEqual('t', variants[3].ref)
        self.assertEqual('t', variants[4].ref)
        self.assertEqual('t', variants[5].ref)
        self.assertEqual('c', variants[0].alt)
        self.assertEqual('c', variants[1].alt)
        self.assertEqual('cc', variants[2].alt)
        self.assertEqual('c', variants[3].alt)
        self.assertEqual('c', variants[4].alt)
        self.assertEqual('c', variants[5].alt)

    def test_call_nucleotide_variants_deletion(self):
        reference_alignment = Sequence('ref', 'tatatta-atat-t')
        alternate_alignment = Sequence('alt', '-a-a--a-a-a---')
        variants = call_nucleotide_variants(reference_alignment, alternate_alignment)

        self.assertEqual(5, len(variants))
        self.assertEqual(0, variants[0].pos)
        self.assertEqual(2, variants[1].pos)
        self.assertEqual(4, variants[2].pos)
        self.assertEqual(8, variants[3].pos)
        self.assertEqual(10, variants[4].pos)
        self.assertEqual('t', variants[0].ref)
        self.assertEqual('t', variants[1].ref)
        self.assertEqual('tt', variants[2].ref)
        self.assertEqual('t', variants[3].ref)
        self.assertEqual('tt', variants[4].ref)
        self.assertEqual('', variants[0].alt)
        self.assertEqual('', variants[1].alt)
        self.assertEqual('', variants[2].alt)
        self.assertEqual('', variants[3].alt)
        self.assertEqual('', variants[4].alt)

    def test_call_nucleotide_variants_insertion(self):
        reference_alignment = Sequence('ref', '-a-a--a-a-a---')
        alternate_alignment = Sequence('alt', 'tatatta-atat-t')
        variants = call_nucleotide_variants(reference_alignment, alternate_alignment)

        self.assertEqual(5, len(variants))
        self.assertEqual(0, variants[0].pos)
        self.assertEqual(1, variants[1].pos)
        self.assertEqual(2, variants[2].pos)
        self.assertEqual(4, variants[3].pos)
        self.assertEqual(5, variants[4].pos)
        self.assertEqual('', variants[0].ref)
        self.assertEqual('', variants[1].ref)
        self.assertEqual('', variants[2].ref)
        self.assertEqual('', variants[3].ref)
        self.assertEqual('', variants[4].ref)
        self.assertEqual('t', variants[0].alt)
        self.assertEqual('t', variants[1].alt)
        self.assertEqual('tt', variants[2].alt)
        self.assertEqual('t', variants[3].alt)
        self.assertEqual('tt', variants[4].alt)

    def test_call_coding_variants(self):
        loci = [NestedGenomicInterval(3, 12, data={'/product': 'X'})]
        nucleotide_variants = [
            Variant('a', 1, 'a', 'd'),
            Variant('a', 3, 'a', 'd'),
            Variant('a', 4, 't', 'd'),
            Variant('a', 5, 'g', 'd'),
            Variant('a', 12, 'a', 't')]
        coding_variants = call_coding_variants(nucleotide_variants, loci)

        self.assertEqual(5, len(coding_variants))
        self.assertIsNone(coding_variants[0])
        self.assertEqual(0, coding_variants[1].pos)
        self.assertEqual(1, coding_variants[2].pos)
        self.assertEqual(2, coding_variants[3].pos)
        self.assertIsNone(coding_variants[4])

    def test_call_codon_variants(self):
        reference = {'X': 'atgatgtgaxxtaa'}
        coding_variants = [
            CodingVariant('X', 0, 'a', 'd'),
            CodingVariant('X', 1, 't', 'd'),
            CodingVariant('X', 2, 'g', 'd'),
            CodingVariant('X', 3, '', 'd'),
        ]
        codon_variants = call_codon_variants(coding_variants, reference)

        self.assertEqual(4, len(codon_variants))
        self.assertEqual(0, codon_variants[0].pos)
        self.assertEqual(0, codon_variants[1].pos)
        self.assertEqual(0, codon_variants[2].pos)
        self.assertEqual(3, codon_variants[3].pos)
        self.assertEqual('atg', codon_variants[0].ref)
        self.assertEqual('atg', codon_variants[1].ref)
        self.assertEqual('atg', codon_variants[2].ref)
        self.assertEqual('atgtga', codon_variants[3].ref)
        self.assertEqual('dtg', codon_variants[0].alt)
        self.assertEqual('adg', codon_variants[1].alt)
        self.assertEqual('atd', codon_variants[2].alt)
        self.assertEqual('datgtgaxxtaa', codon_variants[3].alt)

    def test_call_amino_acid_variants(self):
        codon_variants = [CodonVariant(0, 'atg', 'atc')]
        call_amino_acid_variants(codon_variants)
