from typing import Sequence, Tuple


class IntervalBinner:
    def __init__(self, minbin=2, maxbin=7):
        self._minbin = minbin
        self._maxbin = maxbin
    
    def get_bin(self, ivl):
        for i in range(self._minbin, self._maxbin + 1):
            bin_level = 10 ** i
            if int(ivl.start / bin_level) == int(ivl.stop / bin_level):
                return int(i * 10 ** (self._maxbin + 1) + int(ivl.start / bin_level))
        return int((self._maxbin + 1) * 10 ** (self._maxbin + 1))

    def get_overlapping_bins(self, ivl) -> Sequence[Tuple[int, int]]:
        res = []
        big_bin = int((self._maxbin + 1) * 10 ** (self._maxbin + 1))
        for i in range(self._minbin, self._maxbin + 1):
            bin_level = 10 ** i
            fr = int(i * 10 ** (self._maxbin + 1) + int(ivl.start / bin_level))
            to = int(i * 10 ** (self._maxbin + 1) + int(ivl.stop / bin_level))
            res.append((fr, to + 1))
        res.append((big_bin, big_bin + 1))
        return res
