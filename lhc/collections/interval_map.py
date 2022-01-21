from collections import defaultdict
from lhc.interval import IntervalBinner


class IntervalMap:
    def __init__(self, key_value_pairs=None):
        self._len = 0
        self._binner = IntervalBinner()
        self._bins = defaultdict(list)
        self._values = defaultdict(list)

        if key_value_pairs is not None:
            for key, value in key_value_pairs:
                self[key] = value

    def __len__(self):
        return self._len

    def __iter__(self):
        for bin_ in self._bins.values():
            for item in bin_:
                yield item

    def __contains__(self, item):
        bins = self._binner.get_overlapping_bins(item)
        for fr, to in bins:
            for bin_ in range(fr, to):
                for set_interval in self._bins[bin_]:
                    if set_interval == item:
                        return True
        return False

    def __setitem__(self, key, value):
        self._len += 1
        bin_ = self._binner.get_bin(key)
        self._bins[bin_].append(key)
        self._values[bin_].append(value)

    def __getitem__(self, item):
        bins = self._binner.get_overlapping_bins(item)
        for fr, to in bins:
            for bin_ in range(fr, to):
                for i, set_interval in enumerate(self._bins[bin_]):
                    if set_interval.overlaps(item):
                        yield self._values[bin_][i]

    def keys(self):
        for bin_ in self._bins.values():
            for item in bin_:
                yield item

    def values(self):
        for bin_ in self._values.values():
            for value in bin_:
                yield value

    def items(self):
        for keys, values in zip(iter(self._bins.items()), iter(self._values.items())):
            for key, value in zip(keys, values):
                yield key, value
