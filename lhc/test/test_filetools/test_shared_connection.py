import pickle
import unittest

from multiprocessing import Pipe, Process
from lhc.filetools.shared_connection import SharedConnection


class TestSharedConnection(unittest.TestCase):
    def test_pickling(self):
        conn, b = Pipe()
        connection = SharedConnection(conn)

        pickled_connection = pickle.dumps(connection)
        restored_connection = pickle.loads(pickled_connection)

        connection.send('a')
        self.assertEqual('a', b.recv())
        restored_connection.send('b')
        self.assertEqual('b', b.recv())
        b.send('a')
        self.assertEqual('a', connection.recv())
        b.send('b')
        self.assertEqual('b', restored_connection.recv())

    def test_sending_raw(self):
        server_conn, worker_conn = Pipe()
        a, b = Pipe()

        process = Process(target=echo, args=(worker_conn,))
        process.start()

        server_conn.send(b)
        self.assertEqual('error', server_conn.recv())

        process.terminate()

    def test_sending_wrapped(self):
        server_conn, worker_conn = Pipe()
        a, b = Pipe()

        process = Process(target=echo, args=(worker_conn,))
        process.start()

        server_conn.send(SharedConnection(b))

        a.send('a')
        self.assertEqual('a', a.recv())

        process.terminate()


def echo(conn):
    try:
        b = conn.recv()
        while True:
            message = b.recv()
            b.send(message)
    except TypeError:
        conn.send('error')


if __name__ == '__main__':
    unittest.main()
