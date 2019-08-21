from unittest import TestCase
from lhc.binf.align import align, Mode


class TestAlignmentModes(TestCase):
    def testGlobalAlignment(self):
        sequence1 = 'atacata'
        sequence2 = 'atagcgcata'

        alignment = align(sequence1, sequence2, Mode.GLOBAL)
        self.assertEqual(str(alignment), 'ata---cata\n|||   ||||\natagcgcata')
        self.assertEqual(alignment.get_score(), 20)

    def testLocalAlignment(self):
        sequence1 = 'ggccg'
        sequence2 = 'ataggccggta'

        alignment = align(sequence1, sequence2, Mode.LOCAL)
        self.assertEqual(str(alignment), 'ggccg\n|||||\nggccg')
        self.assertEqual(alignment.get_score(), 25)

    def testSemiGlobalAlignment(self):
        sequence1 = 'ggccg'
        sequence2 = 'ataggccggata'

        alignment = align(sequence1, sequence2, Mode.SEMI)
        self.assertEqual(str(alignment), '---ggccg----\n   |||||    \nataggccggata')
        self.assertEqual(alignment.get_score(), 25)
