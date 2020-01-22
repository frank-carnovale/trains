
from .context import trains

import unittest

class RunQueries(unittest.TestCase):

    def test_a(self):
        """The exact test-case query set given in the specifications"""
        n = trains.Network()
        n.load_graph('tests/data/graph1')
        n.generate_trips()

        for path, EXPECTED_DISTANCE in [
                        ('A-B-C',      9  ),
                        ('A-D',        5  ),
                        ('A-D-C',      13 ),
                        ('A-E-B-C-D',  22 ),
                        ('A-E-D',      'NO SUCH ROUTE' )
                    ]:
            msg = "expected distance {0}".format(EXPECTED_DISTANCE)
            self.assertEqual(n.distance_of_trip(path), EXPECTED_DISTANCE, msg)

        EXPECTED_COUNT = 2
        trips = n.trips_by_stops('C', 'C', 0, 3)
        msg = "#6 expected number of trips {0}".format(EXPECTED_COUNT)
        self.assertEqual(len(trips), EXPECTED_COUNT, msg)

        EXPECTED_COUNT = 3
        trips = n.trips_by_stops('A', 'C', 4, 4)
        msg = "#7 expected number of trips {0}".format(EXPECTED_COUNT)
        self.assertEqual(len(trips), EXPECTED_COUNT, msg)

        EXPECTED_DISTANCE = 9
        trip = n.shortest_trip('A', 'C')
        msg = "#8 expected distance {0}".format(EXPECTED_DISTANCE)
        self.assertEqual(trip.distance, EXPECTED_DISTANCE, msg)

        EXPECTED_DISTANCE = 9
        trip = n.shortest_trip('B', 'B')
        msg = "#9 expected distance {0}".format(EXPECTED_DISTANCE)
        self.assertEqual(trip.distance, EXPECTED_DISTANCE, msg)

        EXPECTED_COUNT = 7
        trips = n.trips_in_distance('C', 'C', 30)
        msg = "#10 expected number of trips {0}".format(EXPECTED_COUNT)
        self.assertEqual(len(trips), EXPECTED_COUNT, msg)

if __name__ == '__main__':
    unittest.main()

