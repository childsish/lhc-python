import unittest

from lhc.binf.alignment.tools.call_variants import call_nucleotide_variants, call_coding_variants
from lhc.binf.genomic_coordinate import NestedGenomicInterval
from lhc.binf.variant import Variant
from lhc.io.sequence import Sequence


class TestCallVariants(unittest.TestCase):
    def test_call_nucleotide_variants_mismatch(self):
        reference_alignment = Sequence('ref', 'atatatta-ata-ta')
        alternate_alignment = Sequence('alt', 'acacacca-aca-ca')
        variants = call_nucleotide_variants(reference_alignment, alternate_alignment)

        self.assertEqual(5, len(variants))
        self.assertEqual(1, variants[0].pos)
        self.assertEqual(3, variants[1].pos)
        self.assertEqual(5, variants[2].pos)
        self.assertEqual(9, variants[3].pos)
        self.assertEqual(11, variants[4].pos)
        self.assertEqual('t', variants[0].ref)
        self.assertEqual('t', variants[1].ref)
        self.assertEqual('tt', variants[2].ref)
        self.assertEqual('t', variants[3].ref)
        self.assertEqual('t', variants[4].ref)
        self.assertEqual('c', variants[0].alt)
        self.assertEqual('c', variants[1].alt)
        self.assertEqual('cc', variants[2].alt)
        self.assertEqual('c', variants[3].alt)
        self.assertEqual('c', variants[4].alt)

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
        reference = 'gaaatgatgtgaaaa'
        loci = [NestedGenomicInterval(3, 12)]
        nucleotide_variants = [Variant(1, 'a', 'd'), Variant(3, 'a', 'd'), Variant(4, 't', 'd'), Variant(5, 'g', 'd'), Variant(12, 'a', 't')]
        coding_variants = call_coding_variants(nucleotide_variants, reference, loci)

        self.assertEqual(5, len(coding_variants))
        self.assertIsNone(coding_variants[0])
        self.assertEqual(0, coding_variants[1].pos)
        self.assertEqual(1, coding_variants[2].pos)
        self.assertEqual(2, coding_variants[3].pos)
        self.assertIsNone(coding_variants[4])
