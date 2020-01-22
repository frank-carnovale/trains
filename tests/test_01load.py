
from .context import trains

import unittest

class LoadGraph(unittest.TestCase):
    """Prove that an input file containing route directives gets loaded and parsed correctly"""

    def test_a(self):
        """Testing successful load and parse, and proves that towns are now in the network"""
        TOWNS_EXPECTED = 5
        n = trains.Network()
        n.load_graph('tests/data/graph1')
        msg = "expected {0} towns loaded".format(TOWNS_EXPECTED)
        self.assertEqual(n.towns_count(), TOWNS_EXPECTED, msg)
        for i in range(ord('A'), ord('E')+1):
            c = chr(i)
            self.assertIn(c, n.town_map, "town {0} is loaded".format(c))
        c = 'F'
        self.assertNotIn(c, n.town_map, "town {0} is NOT loaded".format(c))

    def test_b(self):
        """Tests expected exception raised when route specifiers invalid"""
        n = trains.Network()
        with self.assertRaisesRegexp(trains.LoadError, "not a valid route-definition"):
            n.load_graph('tests/data/graph2')

    def test_c(self):
        """Tests expected exception raised when given route previously loaded"""
        n = trains.Network()
        with self.assertRaisesRegexp(trains.LoadError, "route definition already known"):
            n.load_graph('tests/data/graph3')

    def test_d(self):
        """Tests expected exception raised when given route is self-referencing"""
        n = trains.Network()
        with self.assertRaisesRegexp(trains.LoadError, "doesn't go anywhere"):
            n.load_graph('tests/data/graph4')

if __name__ == '__main__':
    unittest.main()
