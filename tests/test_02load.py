
from .context import trains

import unittest

class GenerateTrips(unittest.TestCase):

    def test_a(self):
        """Prove the solution space of all trip paths gets generated"""
        TRIPS_EXPECTED = 1259
        n = trains.Network()
        n.load_graph('tests/data/graph1')
        n.generate_trips()
        msg = "expected {0} trips generated".format(TRIPS_EXPECTED)
        self.assertEqual(n.trips_count(), TRIPS_EXPECTED, msg)

if __name__ == '__main__':
    unittest.main()
