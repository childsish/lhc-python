import unittest

from lhc.collections.interval_tree import IntervalTree
from lhc.interval import Interval


class TestIntervalTree(unittest.TestCase):
    def test_init(self):
        ivls = [Interval(0, 10), Interval(2, 30), Interval(3, 20), Interval(5, 7), Interval(9, 15),
                Interval(20, 25), Interval(21, 22), Interval(25, 31), Interval(35, 39), Interval(36, 39)]
        tree = IntervalTree(ivls)
        
        self.assertEqual(tree.left, None)
        self.assertEqual(tree.right, None)
        self.assertEqual(tree.ivls, ivls)
        
    def test_initDeepTree(self):
        ivls = [Interval(0, 10), Interval(2, 30), Interval(3, 20), Interval(5, 7), Interval(9, 15), Interval(20, 25),
                Interval(21, 22), Interval(25, 31), Interval(35, 39), Interval(36, 39)]
        tree = IntervalTree(ivls, minbucket=1)
        
        self.assertEqual({Interval(2, 30), Interval(3, 20)}, set(tree.ivls))
        self.assertAlmostEqual(19.5, tree.mid)
        self.assertEqual({Interval(0, 10), Interval(5, 7), Interval(9, 15)}, set(tree.left.ivls))
        self.assertEqual({Interval(20, 25), Interval(21, 22), Interval(25, 31), Interval(35, 39), Interval(36, 39)},
                          set(tree.right.ivls))
        self.assertIsNone(tree.left.left)
        self.assertIsNone(tree.left.right)
        self.assertIsNone(tree.right.left)
        self.assertIsNone(tree.right.right)
    
    def test_intersect(self):
        ivls = [Interval(0, 10), Interval(2, 30), Interval(3, 20), Interval(5, 7), Interval(9, 15), Interval(20, 25),
                Interval(21, 22), Interval(25, 31), Interval(35, 39), Interval(36, 39)]
        tree = IntervalTree(ivls)
        self.assertEqual({Interval(2, 30), Interval(3, 20), Interval(20, 25), Interval(21, 22), Interval(25, 31)},
                          set(tree.intersect(Interval(15, 30))))

if __name__ == '__main__':
    unittest.main()
