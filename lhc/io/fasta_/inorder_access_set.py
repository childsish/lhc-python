import bisect

from itertools import chain
from lhc.interval import Interval


class FastaInOrderAccessSet(object):
    def __init__(self, fileobj):
        self.starts = []
        self.stops = []
        self.buffer = []

        self.fileobj = fileobj
        self.chr = fileobj.next().split()[0][1:]
        self.start = 0

    def fetch(self, chr, start, stop):
        start = (chr, start)
        stop = (chr, stop)

        current_chr = self.chr
        current_start = self.start
        for line in self.fileobj:
            if line.startswith('>'):
                current_chr = line.split()[0][1:]
                current_start = 0
                continue

            line = line.strip()
            key = Interval((current_chr, current_start), (current_chr, current_start + len(line)))
            if key.start >= stop:
                self.fileobj = chain([line], self.fileobj)
                break
            self.starts.append(key.start)
            self.stops.append(key.stop)
            self.buffer.append(line)
            current_start += len(line)
        self.chr = current_chr
        self.start = current_start

        cut_index = bisect.bisect_right(self.stops, start)
        self.starts = self.starts[cut_index:]
        self.stops = self.stops[cut_index:]
        self.buffer = self.buffer[cut_index:]

        index = bisect.bisect_left(self.starts, stop)
        return ''.join(self.buffer[:index])[start[1] - self.starts[0][1]:stop[1] - self.starts[0][1]]
