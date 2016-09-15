import unittest

from lhc.collections import SortedDict


class TestSortedDict(unittest.TestCase):
    def test_init(self):
        sd = SortedDict([(2, 'a'), (3, 'b'), (1, 'c')])

        self.assertEqual(list(sd.items()), [(1, 'c'), (2, 'a'), (3, 'b')])

    def test_setGet(self):
        sd = SortedDict()
        sd[1] = 'b'
        sd[3] = 'c'
        sd[2] = 'a'
        
        self.assertEqual(sd[1], 'b')
        self.assertEqual(sd[2], 'a')
        self.assertEqual(sd[3], 'c')
    
    def test_popHighest(self):
        sd = SortedDict()
        sd[1] = 'b'
        sd[3] = 'c'
        sd[2] = 'a'
        
        self.assertEqual(sd.pop_highest(), (3, 'c'))
    
    def test_popLowest(self):
        sd = SortedDict()
        sd[1] = 'b'
        sd[3] = 'c'
        sd[2] = 'a'
        
        self.assertEqual(sd.pop_lowest(), (1, 'b'))
    
    def test_iterKeys(self):
        sd = SortedDict()
        sd[1] = 'b'
        sd[3] = 'c'
        sd[2] = 'a'
        
        it = iter(sd)
        
        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        self.assertEqual(next(it), 3)
        
    def test_iterValues(self):
        sd = SortedDict()
        sd[1] = 'b'
        sd[3] = 'c'
        sd[2] = 'a'
        
        it = iter(sd.values())
        
        self.assertEqual(next(it), 'b')
        self.assertEqual(next(it), 'a')
        self.assertEqual(next(it), 'c')

if __name__ == "__main__":
    unittest.main()
