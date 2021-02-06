from data_cleaning.graph import Graph


def test_graph():
    g = Graph()
    g.add_edge(1, 0)
    g.add_edge(0, 3)
    g.add_edge(3, 19)
    g.add_edge(19, 0)
    g.add_edge(0, 155)
    g.add_edge(155, 1000)
    g.add_edge(22, 44)
    g.add_edge(44, 55)
    g.add_edge(5, 5555)

    assert sorted(map(lambda grp: sorted(grp), g.find_grps())) == sorted(
        (
            sorted((0, 1, 3, 19, 155, 1000)),
            sorted((22, 44, 55)),
            sorted((5, 5555)),
        )
    )
