from multiprocessing.reduction import reduce_pipe_connection


class SharedConnection(object):
    def __init__(self, connection):
        self.connection = connection

    def __getattr__(self, attribute):
        return getattr(self.connection, attribute)

    def __getstate__(self):
        return reduce_pipe_connection(self.connection)

    def __setstate__(self, state):
        self.connection = state[0](*state[1])
