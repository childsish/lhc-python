import unittest

from lhc.entities.locus import Locus
from lhc.cli.loci.view import view


class TestView(unittest.TestCase):
    def test_view(self):
        intervals = list(view((Locus(0, 100), Locus(50, 150))))

        self.assertEqual(intervals, [Locus(0, 100), Locus(50, 150)])
