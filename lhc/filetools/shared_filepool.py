import gzip

from multiprocessing import Pipe, Process
from shared_connection import SharedConnection
from shared_file import SharedFile


def shared_file_worker(conn, chunk_size=2 ** 16):
    try:
        files = {}
        while True:
            message, args = conn.recv()
            if message == 'stop':
                break

            filename = args['filename']
            if message == 'open':
                mode = args['mode']
                files[filename] = gzip.open(filename, mode) if filename.endswith('.gz') else open(filename, mode)
                conn.send('opened')
            elif message == 'read':
                bytes = args['bytes'] if 'bytes' in args else chunk_size
                conn.send(files[filename].read(bytes))
            elif message == 'write':
                bytes = args['bytes']
                files[filename].write(bytes)
                conn.send('written')
            elif message == 'close':
                files[filename].close()
                conn.send('closed')
            else:
                error = 'unknown command {}'.format(message)
                conn.send(error)
                raise ValueError(error)
    except Exception, e:
        import sys
        sys.stderr.write(str(e))
        conn.send(e.message)


class SharedFilePool(object):

    __slots__ = ('files', 'conn', 'process')

    def __init__(self, chunk_size=2 ** 16):
        self.files = []
        self.conn, conn = Pipe()
        self.conn = SharedConnection(self.conn)
        self.process = Process(target=shared_file_worker, args=(conn, chunk_size))
        self.process.start()

    def join(self):
        for file in self.files:
            file.close()
        self.conn.send(('stop', None))
        self.process.join()

    def terminate(self):
        self.process.terminate()

    def open(self, filename, mode='r'):
        res = SharedFile(filename, self.conn, mode)
        self.files.append(res)
        return res

    def read(self, filename, bytes=2 ** 16):
        return self.files[filename].read(bytes)

    def write(self, filename, bytes):
        return self.files[filename].write(bytes)

    def close(self, filename):
        return self.files[filename].close()

    def __getstate__(self):
        return self.files, self.conn, self.process

    def __setstate__(self, state):
        self.files, self.conn, self.process = state
