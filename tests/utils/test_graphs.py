from unittest import TestCase

from pyxsdata.utils.graphs import strongly_connected_components


class GraphsTests(TestCase):
    def test_strongly_connected_components(self) -> None:
        edges = {
            "a": ["b", "c"],
            "b": ["c"],
            "c": ["b"],
            "d": ["a", "b"],
        }
        sccs = list(strongly_connected_components(edges))
        self.assertIn({"b", "c"}, sccs)
        self.assertIn({"a"}, sccs)
        self.assertIn({"d"}, sccs)
