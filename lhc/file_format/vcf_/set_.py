from lhc.indices.index import Index
from lhc.indices.exact_key import ExactKeyIndex
from lhc.indices.overlapping_interval import OverlappingIntervalIndex
from lhc.interval import Interval

class VcfSet(object):
    def __init__(self, iterator):
        self.data = list(iterator)
        self.ivl_index = Index((ExactKeyIndex, OverlappingIntervalIndex))
        for i, variant in enumerate(iterator):
            ivl = Interval(variant.pos, variant.pos + len(variant.ref))
            self.ivl_index[(variant.chr, ivl)] = i

    def __getitem__(self, key):
        if hasattr(key, 'chr') and hasattr(key, 'pos'):
            length = len(key.ref) if hasattr(key, 'ref') else 1
            ivl = Interval(key.pos, key.pos + length)
            idxs = self.ivl_index[(key.chr, ivl)]
        elif hasattr(key, 'chr') and hasattr(key, 'start') and hasattr(key, 'stop'):
            idxs = self.ivl_index[(key.chr, key)]
        else:
            raise NotImplementedError('Variant set random access not implemented for type: %s'%type(key))
        return [self.data[v] for k, v in idxs]