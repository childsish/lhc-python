from collections import namedtuple

FastaLine = namedtuple('FastaLine', ('hdr', 'seq', 'start', 'stop'))


class FastaIterator(object):
    """
    A line iterator that puts a limit on the line size (some fasta files put the entire genome on one line). Headers
    retain full length.
    """
    def __init__(self, fileobj, threshold=2**16):
        self.fileobj = fileobj
        self.threshold = threshold
        self.hdr = None
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        line = self.fileobj.readline(self.threshold)
        while line == '\n':
            line = self.fileobj.readline(self.threshold)
        if line.startswith('>'):
            if not line.endswith('\n'):
                line += self.fileobj.readline()
            self.hdr = line.strip()
            self.pos = 0
            line = self.fileobj.readline(self.threshold)
            while line == '\n':
                line = self.fileobj.readline(self.threshold)
        line = line.strip()
        res = FastaLine(self.hdr, line.strip(), self.pos, self.pos + len(line))
        self.pos += len(line)
        return res


class FastaEntry(namedtuple('FastaEntry', ('hdr', 'seq'))):
    def __str__(self):
        """
        Represent the entry as a string. Only intended for entries with short sequences.

        :return: The fasta entry as a string
        """
        return '{}\n{}\n'.format(self.hdr, self.seq)


class FastaEntryIterator(object):
    def __init__(self, iterator, hdr_parser=None):
        self.iterator = iterator
        self.hdr_parser = (lambda x: x) if hdr_parser is None else hdr_parser
        self.line = next(self.iterator)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.line is None:
            raise StopIteration()

        seq = []
        for line in self.iterator:
            if line.startswith('>'):
                hdr = self.hdr_parser(self.line[1:].strip())
                self.line = line
                return FastaEntry(hdr, ''.join(seq))
            seq.append(line.strip())
        hdr = self.hdr_parser(self.line[1:].strip())
        self.line = None
        return FastaEntry(hdr, ''.join(seq))

    def close(self):
        if hasattr(self.iterator, 'close'):
            self.iterator.close()

    def __del__(self):
        self.close()
