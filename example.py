from pygraph import Graph


def test_digraph():
    g = Graph)
    g.set_vertex_color(1, "red")
    g.add_edge(1, 2)
    g.add_edge(1, 3, label="test")
    g.add_edge(3, 2, color="blue")
    g.add_edge(3, 4)
    g.add_edge(4, 2, color="red", label="_test")
    g.add_edge("1", 2)
    g.add_edge(4, 1)
    print(g.get_source())
    g.view()

    g.del_edge(1, 2)
    g.del_edge(10, 30)
    g.del_edge(1, 3, label="test_")
    g.del_edge(1, 3, label="test")
    print(g.get_source())
    g.del_vertex_color(1, "red")
    g.view()

    g.set_vertex_shape(1, "box")
    g.set_vertex_shape(1, "box")
    g.set_vertex_shape(2, "diamond")
    print(g.get_source())
    g.view()

    g.del_vertex_shape(1, "box")
    g.del_vertex_shape(2, "box")
    print(g.get_source())
    g.view()


def test_graph():
    g = Graph("graph")
    g.add_edge(1, 2)
    g.add_edge(2, 1)
    g.add_edge(1, 3, label="test")
    g.add_edge(3, 2, color="blue")
    g.add_edge(3, 4)
    g.add_edge(4, 2)
    g.add_edge(1, 2)
    g.add_edge(4, 1)
    print(g.get_source())
    g.view()
    g.del_edge(1, 2)
    g.del_edge(10, 30)
    g.del_edge(1, 3, label="test_")
    g.del_edge(1, 3, label="test")
    print(g.get_source())
    g.view()


def main():
    test_digraph()
    test_graph()


if __name__ == "__main__":
    main()
