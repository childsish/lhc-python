class SharedFile(object):
    def __init__(self, filename, mode='r'):
        self.filepos = 0

        self.filename = filename
        self.mode = mode

        self.fileobj = open(filename, mode)

    def __iter__(self):
        return self

    def next(self):
        res = self.fileobj.next()
        self.filepos += len(res)
        return res

    def read(self, n):
        res = self.fileobj.read(n)
        self.filepos = self.fileobj.tell()
        return res

    def write(self, b):
        self.fileobj.write(b)
        self.filepos = self.fileobj.tell()

    def tell(self):
        return self.filepos

    def __del__(self):
        if hasattr(self, 'fileobj') and not self.fileobj.closed:
            self.fileobj.close()

    def __getstate__(self):
        return self.filepos, self.filename, self.mode

    def __setstate__(self, state):
        self.filepos, self.filename, self.mode = state
        self.fileobj = open(self.filename, self.mode)
        self.fileobj.seek(self.filepos)
