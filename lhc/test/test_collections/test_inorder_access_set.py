import unittest

from lhc.collections.inorder_access_set import InOrderAccessSet


class TestInOrderAccessSet(unittest.TestCase):
    def setUp(self):
        self.points = [0, 10, 20, 30, 40, 50]
        self.key_points = [(0, 0, 'q'), (10, 0, 'w'), (10, 10, 'e'), (20, 0, 'r'), (20, 10, 't'), (20, 20, 'y')]

    def test_getByInterval(self):
        set_ = InOrderAccessSet(iter(self.points))

        self.assertEqual(set_[0:10], [0])
        self.assertEqual(set_[10:21], [10, 20])
        self.assertEqual(set_[30:51], [30, 40, 50])
        self.assertEqual(set_[50:51], [50])

if __name__ == '__main__':
    unittest.main()
