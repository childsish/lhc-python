import unittest

from lhc.graph.graph import Graph, Edge


class TestGraph(unittest.TestCase):
    def test_init_noarg(self):
        graph = Graph()

        self.assertEquals('G', graph.name)
        self.assertEquals(0, len(list(graph.es)))
        self.assertEquals(0, len(graph))

    def test_init_arg(self):
        graph = Graph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('d', 'a')])

        self.assertEquals('G', graph.name)
        self.assertEquals(4, len(list(graph.es)))
        self.assertEquals(4, len(graph))

    def test_add_vertex(self):
        graph = Graph()
        v1 = graph.add_vertex('a')
        v2 = graph.add_vertex('b')
        e = graph.add_edge(v1, v2)

        self.assertEquals('G', graph.name)
        self.assertEquals(1, len(list(graph.es)))
        self.assertEquals(2, len(graph))
        self.assertEquals({Edge(v1, v2)}, set(graph.es))

    def test_get_family(self):
        graph = Graph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('d', 'a')])

        self.assertEquals({'b', 'c'}, graph.get_children('a'))
        self.assertEquals({'b'}, graph.get_parents('d'))

    def test_decompose(self):
        graph = Graph()
        graph.add_edge('a', 'b')
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'd')
        graph.add_edge('d', 'a')
        graph.add_edge('e', 'f')
        graph.add_edge('e', 'g')

        graphs = list(graph.decompose())
        graph1, graph2 = (graphs[0], graphs[1]) if 'a' in graphs[0].adjacency else (graphs[1], graphs[0])

        self.assertEquals({Edge('a', 'b'), Edge('a', 'c'), Edge('b', 'd'), Edge('d', 'a')}, set(graph1.es))
        self.assertEquals({'a', 'b', 'c', 'd'}, set(graph1.vs))
        self.assertEquals({Edge('e', 'f'), Edge('e', 'g')}, set(graph2.es))
        self.assertEquals({'e', 'f', 'g'}, set(graph2.vs))


if __name__ == '__main__':
    unittest.main()
