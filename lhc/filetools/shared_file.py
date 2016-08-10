import gzip

from shared_connection import SharedConnection


def file_worker(conn, size=2 ** 16):
    files = {}
    while True:
        message, data = conn.recv()
        if message == 'open':
            mode = data['mode'] if 'mode' in data else 'r'
            files[data['filename']] = gzip.open(data['filename'], mode) if data['filename'].endswith('.gz') else\
                open(data['filename'], mode)
        elif message == 'read':
            size_ = data['size'] if 'size' in data else size
            buffer = files[data['filename']].read(size_)
            conn.send(buffer)
        elif message == 'stop':
            break


class SharedFile(object):
    def __init__(self, filename, conn, mode='r'):
        self.pos = 0
        self.buffer = ''

        self.filename = filename
        self.conn = conn if isinstance(conn, SharedConnection) else SharedConnection(conn)

        self.conn.send(('open', {
            'filename': filename,
            'mode': mode
        }))

    def __iter__(self):
        return self

    def next(self):
        index = self.buffer.find('\n', self.pos)
        if index == -1:
            buffers = [self.buffer[self.pos:]]
            self.pos = 0
            pos = 0
            while index == -1:
                pos += len(buffers[-1])
                self.conn.send(('read', {'filename': self.filename}))
                buffer = self.conn.recv()
                if buffer == '':
                    if buffers[-1] == '':
                        raise StopIteration
                    buffer = self.buffer
                    self.buffer = ''
                    return buffer
                index = buffer.find('\n')
                buffers.append(buffer)
            index += pos
            self.buffer = ''.join(buffers)
        pos = self.pos
        self.pos = index + 1
        return self.buffer[pos:index + 1]
