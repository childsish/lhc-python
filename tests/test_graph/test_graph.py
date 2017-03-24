import unittest

from collections import namedtuple
from lhc.graph.graph import Graph, Edge


class TestGraph(unittest.TestCase):
    def test_init_arg(self):
        graph = Graph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('d', 'a')], directed=False)

        self.assertEqual('G', graph.name)
        self.assertEqual(4, len(list(graph.es)))
        self.assertEqual(4, len(graph))

    def test_add_edge(self):
        graph = Graph()

        graph.add_edge('a', 'b')
        graph.add_edge('b', 'c')

        self.assertEqual({'a', 'b', 'c'}, set(graph.vs))
        self.assertEqual(2, len(list(graph.es)))
        self.assertIn(Edge('b', 'c'), set(graph.es))

    def test_graph_owns_vertices(self):
        class Vertex(object):
            def __init__(self, x):
                self.x = x

            def __str__(self):
                return str(self.x)

            def __hash__(self):
                return hash(self.x)

            def __eq__(self, other):
                return self.x == other.x

        a1 = Vertex(1)
        a2 = Vertex(1)
        b = Vertex(2)
        graph = Graph()

        graph.add_vertex(a1)
        graph.add_vertex(b)
        graph.add_edge(a2, b)
        a2.x = 3

        self.assertEqual(2, len(graph))
        self.assertEqual(1, list(graph.adjacency[b].parents)[0].x)

    def test_get_neighbours(self):
        graph = Graph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('d', 'a')], directed=False)

        self.assertEqual({'b', 'c', 'd'}, graph.get_neighbours('a'))

    def test_decompose(self):
        graph = Graph(directed=False)
        graph.add_edge('a', 'b')
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'd')
        graph.add_edge('d', 'a')
        graph.add_edge('e', 'f')
        graph.add_edge('e', 'g')

        graphs = list(graph.decompose())
        graph1, graph2 = (graphs[0], graphs[1]) if 'a' in graphs[0].vs else (graphs[1], graphs[0])

        self.assertEqual({Edge('a', 'b'), Edge('a', 'c'), Edge('b', 'd'), Edge('d', 'a')}, set(graph1.es))
        self.assertEqual({'a', 'b', 'c', 'd'}, set(graph1.vs))
        self.assertEqual({Edge('e', 'f'), Edge('e', 'g')}, set(graph2.es))
        self.assertEqual({'e', 'f', 'g'}, set(graph2.vs))

    def test_update(self):
        g1 = Graph(directed=False)
        g1.add_edge('a', 'b')
        g1.add_edge('a', 'c')
        g2 = Graph(directed=False)
        g2.add_edge('b', 'd')
        g2.add_edge('b', 'e')

        g1.update(g2)

        self.assertEqual({Edge('a', 'b'), Edge('a', 'c'), Edge('b', 'd'), Edge('b', 'e')}, set(g1.es))
        self.assertEqual({'a', 'b', 'c', 'd', 'e'}, set(g1.vs))

if __name__ == '__main__':
    unittest.main()
