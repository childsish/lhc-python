import unittest


from lhc.io.locus.embl import EmblFile


class TestEmblFile(unittest.TestCase):
    def test_parse_location(self):
        embl_file = EmblFile()

        interval = embl_file.parse_location('467')
        self.assertEqual(466, interval.start.position)
        interval = embl_file.parse_location('340..565')
        self.assertEqual(339, interval.start.position)
        self.assertEqual(565, interval.stop.position)
        interval = embl_file.parse_location('<1..888')
        self.assertEqual(0, interval.start.position)
        self.assertEqual(888, interval.stop.position)
        interval = embl_file.parse_location('1..>888')
        self.assertEqual(0, interval.start.position)
        self.assertEqual(888, interval.stop.position)
        interval = embl_file.parse_location('102.110')
        self.assertEqual(101, interval.start.position)
        self.assertEqual(110, interval.stop.position)
        interval = embl_file.parse_location('123^124')
        self.assertEqual(122, interval.start.position)
        self.assertEqual(124, interval.stop.position)
        interval = embl_file.parse_location('join(12..78,134..202)')
        self.assertEqual(11, interval.start.position)
        self.assertEqual(202, interval.stop.position)
        self.assertEqual(11, interval.children[0].start.position)
        self.assertEqual(78, interval.children[0].stop.position)
        self.assertEqual(133, interval.children[1].start.position)
        self.assertEqual(202, interval.children[1].stop.position)
        interval = embl_file.parse_location('complement(34..126)')
        self.assertEqual(33, interval.start.position)
        self.assertEqual(126, interval.stop.position)
        self.assertEqual('-', interval.strand)
        interval = embl_file.parse_location('complement(join(2691..4571,4918..5163))')
        self.assertEqual(2690, interval.start.position)
        self.assertEqual(5163, interval.stop.position)
        self.assertEqual('-', interval.strand)
        interval = embl_file.parse_location('join(complement(4918..5163),complement(2691..4571))')
        self.assertEqual(2690, interval.start.position)
        self.assertEqual(5163, interval.stop.position)

    @unittest.skip
    def test_parse_location_with_sequence_name(self):
        embl_file = EmblFile()

        interval = embl_file.parse_location('J00194.1:100..202')
        self.assertEqual(467, interval.start.position)
        interval = embl_file.parse_location('join(1..100,J00194.1:100..202)')
        self.assertEqual(467, interval.start.position)

    def test_parse_qualifiers(self):
        embl_file = EmblFile()
        qualifiers = embl_file.parse_qualifiers(
            [
                ';FT                 /product="ORF1"',
                ';FT                 /translation="MGKKQNRKTGNSKTQSASPPPKERSSSPATEQSWME"',
                ';FT                 /frame=3'
            ])
        self.assertEqual(
            {'product': 'ORF1', 'translation': 'MGKKQNRKTGNSKTQSASPPPKERSSSPATEQSWME', 'frame': 3},
            qualifiers)
        self.assertEqual(
            {'translation': 'NDFDELREEGFRRSNYSELREDIQTKGKEVENFEKNLEECITRITNTEKC'},
            embl_file.parse_qualifiers(
                [
                    ';FT                 /translation="NDFDELREEGFRRSNYSELREDIQ',
                    ';FT                 TKGKEVENFEKNLEECITRITNTEKC"'
                ]))
