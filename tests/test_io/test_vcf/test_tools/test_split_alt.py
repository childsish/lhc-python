import unittest

from lhc.io.vcf.iterator import Variant
from lhc.io.vcf.tools.split_alt import _split_samples, _split_dict, _split_variant


class TestSplitAlt(unittest.TestCase):
    def test_split_dict(self):
        self.assertEqual(
            [
                {'DP': '1000', 'AO': '300'},
                {'DP': '1000', 'AO': '100'}
            ],
            _split_dict(
                {'DP': '1000', 'AO': '300,100'},
                2
            )
        )

        self.assertEqual(
            [
                {'DP': '1000', 'AO': '300', 'AF': '0.3'},
                {'DP': '1000', 'AO': '100', 'AF': '0.1'}
            ],
            _split_dict(
                {'DP': '1000', 'AO': '300,100', 'AF': '0.3,0.1'},
                2
            )
        )

    def test_split_samples(self):
        self.assertEqual(
            [
                {
                    's1': {'DP': '1000', 'AO': '300', 'AF': '0.3'},
                    's2': {'DP': '1000', 'AO': '400', 'AF': '0.4'}
                },
                {
                    's1': {'DP': '1000', 'AO': '100', 'AF': '0.1'},
                    's2': {'DP': '1000', 'AO': '200', 'AF': '0.2'}
                }
            ],
            _split_samples(
                {
                    's1': {'DP': '1000', 'AO': '300,100', 'AF': '0.3,0.1'},
                    's2': {'DP': '1000', 'AO': '400,200', 'AF': '0.4,0.2'}
                },
                2
            )
        )

    def test_split_variant(self):
        variant = Variant(('1', 100), '', 'G', ['GAAC', 'C'], '', '', {'f1': '0,1', 'f2': '3'}, ['DP', 'AO', 'AF'], {
            's1': {'DP': '1000', 'AO': '300,100', 'AF': '0.3,0.1'},
            's2': {'DP': '1000', 'AO': '400,200', 'AF': '0.4,0.2'}
        })

        v1, v2 = _split_variant(variant)

        self.assertEqual(Variant(('1', 100), '', 'G', 'GAAC', '', '', {'f1': '0', 'f2': '3'}, ['DP', 'AO', 'AF'], {
            's1': {'DP': '1000', 'AO': '300', 'AF': '0.3'},
            's2': {'DP': '1000', 'AO': '400', 'AF': '0.4'}
        }), v1)
        self.assertEqual(Variant(('1', 100), '', 'G', 'C', '', '', {'f1': '1', 'f2': '3'}, ['DP', 'AO', 'AF'], {
            's1': {'DP': '1000', 'AO': '100', 'AF': '0.1'},
            's2': {'DP': '1000', 'AO': '200', 'AF': '0.2'}
        }), v2)

    def test_split_variant_no_samples(self):
        variant = Variant(('1', 100), '', 'G', ['GAAC', 'C'], '', '', {'f1': '0,1', 'f2': '3'}, [], {})

        v1, v2 = _split_variant(variant)
        self.assertEqual(v1.samples, {})
        self.assertEqual(v2.samples, {})


if __name__ == '__main__':
    unittest.main()
