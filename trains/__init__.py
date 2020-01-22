
import sys
from .core import Network, Trip, Town, Route, LoadError

if "ps1" in dir(sys): # identifies interactive mode
    print "Welcome to the Trains package."
    print
    print " Interactive Mode Usage:"
    print "\tnetwork = Network()                            Creates a new (empty) network"
    print "\tnetwork.load_graph(FILE)                       Loads graph information from FILE"
    print " After load_graph().."
    print "\tnetwork.towns_count()                          Total towns"
    print "\tprint network.dump()                           Town Routes report"
    print "\tnetwork.generate_trips()                       Generate all valid trips."
    print " After generate_trips().."
    print "\tnetwork.trips_count()                          Total trips"
    print "\tnetwork.all_trips()                            Full report of all available trips"
    print "\tnetwork.distance_of_trip('A-B-C')              Get distance of proposed trip"
    print "\ttrips=network.trips_by_stops('A', 'B', 1, 5)   Show trips from A to B having between 1 and 5 stops"
    print "\ttrips=network.shortest_trip('A', 'B')          Show shortest trip from A to B"
    print "\ttrips=network.trips_in_distance('A', 'B', 20)  Show trips from A to B with total distance under 20"
    print

