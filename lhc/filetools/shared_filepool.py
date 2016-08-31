import gzip

from multiprocessing import Pipe, Process, Manager
from .shared_connection import SharedConnection
from .shared_file import SharedFile


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
            elif message == 'readline':
                bytes = args['bytes']
                conn.send(files[filename].readline(bytes))
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
    except Exception as e:
        import sys
        sys.stderr.write(str(e))
        conn.send(e.message)


class SharedFilePool(object):

    def __init__(self, chunk_size=2 ** 16):
        self.manager = Manager()
        with_master, with_slave = Pipe()
        self.files = SharedFilePoolStore(SharedConnection(with_slave, self.manager.Lock()))
        self.process = Process(target=shared_file_worker, args=(with_master, chunk_size))
        self.process.start()

    def join(self):
        self.files.close()
        self.process.join()

    def terminate(self):
        self.process.terminate()

    def get_file_manager(self):
        return self.files


class SharedFilePoolStore(object):

    __slots__ = ('files', 'conn')

    def __init__(self, conn):
        self.files = []
        self.conn = conn

    def open(self, filename, mode='r'):
        res = SharedFile(filename, self.conn, mode)
        self.files.append(res)
        return res

    def read(self, filename, bytes=2 ** 16):
        return self.files[filename].read(bytes)

    def write(self, filename, bytes):
        return self.files[filename].write(bytes)

    def close(self, filename=None):
        if filename is None:
            for file in self.files:
                file.close()
        else:
            self.files[filename].close()
        self.conn.send(('stop', None))

    def __getstate__(self):
        return self.files, self.conn

    def __setstate__(self, state):
        self.files, self.conn = state
