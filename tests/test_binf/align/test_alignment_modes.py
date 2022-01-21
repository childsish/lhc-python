import unittest

try:
    from lhc.binf.align import align, Mode
    skip = False
except ImportError:
    align = None
    Mode = None
    skip = True


@unittest.skipIf(skip, 'unable to import numpy')
class TestAlignmentModes(unittest.TestCase):
    def test_global_alignment(self):
        sequence1 = 'atacata'
        sequence2 = 'atagcgcata'

        alignment = align(sequence1, sequence2, Mode.GLOBAL)
        self.assertEqual(str(alignment), 'ata---cata\n|||   ||||\natagcgcata')
        self.assertEqual(alignment.get_score(), 20)

    def test_local_alignment(self):
        sequence1 = 'ggccg'
        sequence2 = 'ataggccggta'

        alignment = align(sequence1, sequence2, Mode.LOCAL)
        self.assertEqual(str(alignment), 'ggccg\n|||||\nggccg')
        self.assertEqual(alignment.get_score(), 25)

    def test_semi_global_alignment(self):
        sequence1 = 'ggccg'
        sequence2 = 'ataggccggata'

        alignment = align(sequence1, sequence2, Mode.SEMI)
        self.assertEqual(str(alignment), '---ggccg----\n   |||||    \nataggccggata')
        self.assertEqual(alignment.get_score(), 25)
