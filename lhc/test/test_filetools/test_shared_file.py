import pickle
import unittest

from multiprocessing import Pipe, Process
from lhc.filetools.shared_file import SharedFile


class TestSharedFile(unittest.TestCase):
    def test_pickling(self):
        a, b = Pipe()
        shared_file = SharedFile('test.txt', b)

        pickled_file = pickle.dumps(shared_file)
        restored_file = pickle.loads(pickled_file)

        a.send('a')
        self.assertEqual('a', shared_file.conn.recv())
        a.send('b')
        self.assertEqual('b', restored_file.conn.recv())

    def test_sending(self):
        server_conn, worker_conn = Pipe()
        a, b = Pipe()

        process = Process(target=echo, args=(worker_conn,))
        process.start()

        server_conn.send(SharedFile('test.txt', b))

        self.assertEqual(('open', {'mode': 'r', 'filename': 'test.txt'}), a.recv())
        a.send('a')
        self.assertEqual('a', a.recv())

        process.terminate()


def echo(conn):
    b = conn.recv()
    while True:
        message = b.conn.recv()
        b.conn.send(message)

if __name__ == '__main__':
    unittest.main()
