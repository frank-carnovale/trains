"""
"Trains" Main Program.
See full documentation at http://octalfutures.com/trains
(authorisation needed)
"""

import sys
from core import Network, LoadError

############################
def _oops(exception_class, value, traceback):
    """Global Exception handler"""
    # notify sysops here! include 'traceback' in the notification.
    # (not yet implemented).
    print "The Trains system encountered this unexpected error:"
    print exception_class, value
    print "Details have been logged and operations have been notified."
    print "Please try again when ready."
    sys.exit()
sys.excepthook = _oops

############################
# Setup
print "'Trains' Main Program."

if len(sys.argv) <= 1:
    print "usage: python trains FILE.."
    print "\twhere the FILEs describe available routes for a Trains network."
    sys.exit()

network = Network()
for infile in sys.argv[1:]:
    print "loading {0}..".format(infile)
    try:
        network.load_graph(infile)
    except LoadError as exception_obj:
        msg = "File {0} was not loaded successfully:\n\t{1}"
        raise Exception(msg.format(file, exception_obj))

print "network has {0} towns".format(network.towns_count())
print

network.generate_trips()

############################
# Q's 1..5
q = 0
for path in ['A-B-C', 'A-D', 'A-D-C', 'A-E-B-C-D', 'A-E-D']:
    q += 1
    print "Q"+str(q), "Distance of", path, "is", network.distance_of_trip(path)
    print

############################
# Q6
trips = network.trips_by_stops('C', 'C', 0, 3)
print "Q6 Routes from C to C with max 3 stops..", len(trips)
for trip in trips:
    print "\t", trip
print

############################
# Q7
trips = network.trips_by_stops('A', 'C', 4, 4)
print "Q7 Routes from A to C with exactly 4 stops..", len(trips)
for trip in trips:
    print "\t", trip
print

############################
# Q8
trip = network.shortest_trip('A', 'C')
print "Q8 From A to C shortest route..", trip.distance, "km"
print "\t", trip
print

############################
# Q9
trip = network.shortest_trip('B', 'B')
print "Q9 From B to B shortest route..", trip.distance, "km"
print "\t", trip
print

############################
# Q10
trips = network.trips_in_distance('C', 'C', 30)
print "Q10 Routes from C to C under distance 30km..", len(trips)
for trip in trips:
    print "\t", trip
print

############################
print "done"
