from unittest import TestCase, main

from lhc.misc.genetic_code import GeneticCodes


class TestGeneticCodes(TestCase):
    def test_integration(self):
        gc = GeneticCodes()

        self.assertIn('Standard', gc.name2id)
        self.assertEqual(gc['Standard']['ttt'], 'F')
        self.assertEqual(gc['Standard']['ggg'], 'G')

if __name__ == '__main__':
    import sys
    sys.exit(main())
