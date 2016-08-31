from .shared_connection import SharedConnection


class SharedFile(object):

    __slots__ = ('pos', 'buffer', 'filename', 'conn')

    def __init__(self, filename, conn, mode='r'):
        self.pos = 0
        self.buffer = b''

        self.filename = filename
        self.conn = conn if isinstance(conn, SharedConnection) else SharedConnection(conn)

        self.conn.send(('open', {
            'filename': filename,
            'mode': mode
        }))
        self.conn.recv()

    def __iter__(self):
        return self

    def __next__(self):
        index = self.buffer.find(b'\n', self.pos)
        if index == -1:
            buffers = [self.buffer[self.pos:]]
            self.pos = 0
            pos = 0
            while index == -1:
                pos += len(buffers[-1])
                self.conn.send(('read', {
                    'filename': self.filename
                }))
                buffer = self.conn.recv()
                if buffer == b'':
                    if buffers[-1] == b'':
                        raise StopIteration
                    buffer = self.buffer
                    self.buffer = b''
                    return buffer
                index = buffer.find(b'\n')
                buffers.append(buffer)
            index += pos
            self.buffer = b''.join(buffers)
        pos = self.pos
        self.pos = index + 1
        return self.buffer[pos:index + 1]

    def read(self, bytes=2 ** 16):
        self.conn.send(('read', {
            'filename': self.filename,
            'bytes': bytes
        }))
        return self.conn.recv()

    def readline(self, bytes=0):
        self.conn.send(('readline', {
            'filename': self.filename,
            'bytes': bytes
        }))
        return self.conn.recv()

    def write(self, bytes):
        self.conn.send(('write', {
            'filename': self.filename,
            'bytes': bytes
        }))
        return self.conn.recv()

    def close(self):
        self.conn.send(('close', {
            'filename': self.filename
        }))
        return self.conn.recv()

    def __getstate__(self):
        return self.pos, self.buffer, self.filename, self.conn

    def __setstate__(self, state):
        self.pos, self.buffer, self.filename, self.conn = state
