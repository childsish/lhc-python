from unittest import TestCase
from lhc.misc.string import get_index_of_approximate_match


class TestString(TestCase):
    def test_get_index_of_approximate_match(self):
        query = 'CTTGAGCATCTGACTTCTGGCTA'
        template = 'ttcattataatcttcaatatttctcttccccacacaaaacttctattatctctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(None, get_index_of_approximate_match(query, template, 0))
        template = 'TTGAGCATCTGACTTCTGGCTActcttccccacacaaaacttctattatctctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(None, get_index_of_approximate_match(query, template, 0))
        template = 'ttcattataatcttcaatatttctcttccccacacaaaacttctattatctctcctccttttctCTTGAGCATCTGACTTCTGGCT'.upper()
        self.assertEqual(None, get_index_of_approximate_match(query, template, 0))

        template = 'CTTGAGCATCTGACTTCTGGCTAtcttccccacacaaaacttctattatctctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(0, get_index_of_approximate_match(query, template, 0))
        template = 'ttcattataatcttcaatatttctctCTTGAGCATCTGACTTCTGGCTActctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(26, get_index_of_approximate_match(query, template, 0))
        template = 'ttcattataatcttcaatatttctcttccccacacaaaacttctattatctctcctccttttcCTTGAGCATCTGACTTCTGGCTA'.upper()
        self.assertEqual(63, get_index_of_approximate_match(query, template, 0))

        template = 'TTGAGCATCTGACTTCTGGCTActcttccccacacaaaacttctattatctctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(-1, get_index_of_approximate_match(query, template, 1))
        template = 'ttcattataatcttcaatatttctctCTTGAGCATNTGACTTCTGGCTActctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(26, get_index_of_approximate_match(query, template, 1))
        template = 'ttcattataatcttcaatatttctctCTTGAGCATNNGACTTCTGGCTActctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(None, get_index_of_approximate_match(query, template, 1))
        template = 'ttcattataatcttcaatatttctcttccccacacaaaacttctattatctctcctccttttctCTTGAGCATCTGACTTCTGGCT'.upper()
        self.assertEqual(64, get_index_of_approximate_match(query, template, 1))

        template = 'TTGAGCATCTGACTTCTGGCTActcttccccacacaaaacttctattatctctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(-1, get_index_of_approximate_match(query, template, 2))
        template = 'TGAGCATCTGACTTCTGGCTAtctcttccccacacaaaacttctattatctctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(-2, get_index_of_approximate_match(query, template, 2))
        template = 'ttcattataatcttcaatatttctctCTTGAGCATNNGACTTCTGGCTActctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(26, get_index_of_approximate_match(query, template, 2))
        template = 'ttcattataatcttcaatatttctctCTTGAGCATNNNACTTCTGGCTActctcctccttttcttcctttttttcttctcttttct'.upper()
        self.assertEqual(None, get_index_of_approximate_match(query, template, 2))
        template = 'ttcattataatcttcaatatttctcttccccacacaaaacttctattatctctcctccttttcttCTTGAGCATCTGACTTCTGGC'.upper()
        self.assertEqual(65, get_index_of_approximate_match(query, template, 2))
