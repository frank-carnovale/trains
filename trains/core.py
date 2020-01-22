# -*- coding: utf-8 -*-
"""Class Library for Trains System"""

import re

# These affect the route traversal algorithm.
# See docstring for Network..
ALLOW_CYCLIC_JOURNEYS = 1
MAXIMUM_STOPS = 10

#######################################
def validate_word(word):
    """Verifies that a single route directive is syntactically ok"""
    match = re.match(r'^([A-Z])([A-Z])(\d+)$', word)
    if not match:
        msg = '"{0}" is not a valid route-definition word'
        raise LoadError(msg.format(word))
    return match.group(1, 2, 3)

#######################################
class LoadError(Exception):
    """A standard exception class for distinguishing
    application-specific load errors.
    """

    def __init__(self, value):
        super(LoadError, self).__init__(value)
        self.value = value
    def __str__(self):
        return self.value

#######################################
class Route:
    """A route in the 'Trains' system.

    We define a 'route' as a single-hop one-way linkage of known distance,
    between two towns.
    """

    def __init__(self, fm_town, to_town, distance):
        """Simple route constructor"""
        self.fm_town = fm_town
        self.to_town = to_town
        self.distance = int(distance)

#######################################
class Town:
    """A town in the 'Trains' system.

    Can also be considered a 'node' in the network graph.
    A town is labelled by a single uppercase alphabetic letter A-Z.
    It is the departure point for uni-directional routes to other towns.
    """

    def __init__(self, alpha):
        """Construct with a single alphabetic letter"""
        self.alpha = alpha
        self.to_map = {}

    def __str__(self):
        """Stringification of a Town object is just
        its single alpha identifier
        """
        return self.alpha

    def dump(self):
        """Dumps the set of routes (i.e. 1-hop linkages out of town)
        belonging to this town.

        Use this as a diagnostic to verify correct loading of the network
        input data for this town.
        """

        output = "Town {0} routes out of town are..\n".format(self.alpha)
        for alpha, route in self.to_map.items():
            output += '\t{0} {1}\n'.format(alpha, route.distance)
        return output

    def add_route(self, to_town, distance, word):
        """Adds a single direct route to another town object.

        :param to_town: destination town
        :param distance: distance (in kms)
        :param word: the original route string from the input file.
        :type to_town: Town object
        :type distance: integer
        :type word: string

        """

        if to_town.alpha in self.to_map:
            msg = '"{0}": route definition already known'
            raise LoadError(msg.format(word))
        self.to_map[to_town.alpha] = Route(self, to_town, distance)

    def generate_trips(self, fm_town, via, distance_so_far, stops_so_far):
        """Given a traversal that began at fm_town,
        and the accumulated distance and stop-count
        to reach this town (self), consult my own to_map to derive
        still more ongoing trips that start from fm_town.

        :param fm_town: original trip departure point.
        :param via: list of towns traversed to get this far.
        :param distance_so_far: accumulated distance travelled so far.
        :param stops_so_far: number of nodes traversed so far.
        :type fm_town: Town object
        :type via: list of town objects
        :type distance_so_far: integer
        :type stops_so_far: integer
        """

        if ALLOW_CYCLIC_JOURNEYS and stops_so_far > MAXIMUM_STOPS:
            return []
        trips = []
        stops = stops_so_far + 1
        for route in self.to_map.values():
            to_town = route.to_town
            if not ALLOW_CYCLIC_JOURNEYS and to_town in via:
                continue
            distance = distance_so_far + route.distance
            trips += [Trip(fm_town, to_town, via, distance, stops)]
            if not ALLOW_CYCLIC_JOURNEYS and fm_town == to_town:
                continue
            via_me_too = via[:]                 # shallow copy of a list
            via_me_too.append(to_town)
            trips += to_town.generate_trips(fm_town, via_me_too,
                                            distance, stops)
        return trips

#######################################
class Trip:
    """A Trip in the 'Trains' system.

    We define a 'trip' as any journey on the network, of one or more stops.

    A trip definition needs the start and end town, and the ordered list of
    stops in between (if any).  We redundantly persist the derived stop-count
    and the total journey distance as attributes.
    """
    def __init__(self, fm_town, to_town, via, distance, stops):
        self.fm_town = fm_town
        self.to_town = to_town
        self.via = via
        self.distance = distance
        self.stops = stops
    def __str__(self):
        """A nice stringify rule showing concise trip info,
        suitable for reports
        """
        fmt = "{0:20} {1:4} km {2:3} stops"
        return fmt.format(self.trip_path(), self.distance, self.stops)
    def trip_path(self):
        """Construct a A-B-C style path showing start, via-towns, and end for
        this trip
        """
        path = [self.fm_town.alpha]
        path += [t.alpha for t in self.via]
        path += [self.to_town.alpha]
        return '-'.join(path)

#######################################
class Network:
    """A Network in the 'Trains' system.

    A network is a simple map of town objects, which in turn contain route
    information.
    """

    def __init__(self):
        """Construct a network with an empty town map and no known trips"""
        self.town_map = {}
        self.trips = []
        self.trips_by_path = {}

    #######################################
    # Report Functions

    def dump(self):
        """Dumps the set of routes (i.e. 1-hop linkages out of town)
        belonging to this town.

        Use this as a diagnostic to verify correct loading of the network input
        data for all towns.
        """

        output = ''
        for alpha, town in self.town_map.items():
            output += 'TOWN ' + alpha + '\n'
            output += town.dump()
        return output

    def towns_count(self):
        """Retrieves count of loaded towns.  Available after 'load_graph()'"""
        return len(self.town_map)

    def trips_count(self):
        """Retrieves count of generated trips.
        Available after 'generate_trips()'
        """
        return len(self.trips)

    def distance_of_trip(self, path):
        """Look-up an A-B-C style trip path and return its distance"""
        if path not in self.trips_by_path:
            return "NO SUCH ROUTE"
        return self.trips_by_path[path].distance

    def all_trips(self):
        """Report the full collection of available trips

        Can be big, especially if cyclic-trips allowed, and max-stops is large.
        """
        print "Total {0} non-iterating trips".format(len(self.trips))
        for trip in self.trips:
            print trip

    def trips_by_stops(self, fm_alpha, to_alpha, min_stops, max_stops):
        """Return all trips from  A to B which have stops-count between
        given min and max
        """
        return [t for t in self.trips
                if  t.stops >= min_stops and t.stops <= max_stops
                and t.fm_town.alpha == fm_alpha
                and t.to_town.alpha == to_alpha]

    def shortest_trip(self, fm_alpha, to_alpha):
        """Return the trip from A to B which has the minimum distance"""
        trips = [t for t in self.trips
                 if  t.fm_town.alpha == fm_alpha
                 and t.to_town.alpha == to_alpha]
        return min(trips, key=lambda t: t.distance)

    def trips_in_distance(self, fm_alpha, to_alpha, max_distance):
        """Return all trips from A to B which are under the given distance"""
        return [t for t in self.trips
                if  t.fm_town.alpha == fm_alpha
                and t.to_town.alpha == to_alpha
                and t.distance < max_distance]

    #######################################
    # Builders

    def generate_trips(self):
        """Traverse all towns in the network and determine all possible routes
        from them.

        Saves all routes in a list and also maps them into an A-B-C style
        path-based dictionary.

        These constants affect the algorithm:

        ALLOW_CYCLIC_JOURNEYS  -- allow cyclic journeys

        MAXIMUM_STOPS          -- limit to number of stops in a trip.
        Only applies when cyclic journeys allowed.
        """

        for fm_town in self.town_map.values():
            self.trips += fm_town.generate_trips(fm_town, [], 0, 0)
        self.trips_by_path = {t.trip_path(): t for t in self.trips}

    def add_town(self, alpha):
        """
        Create a town object corresponding to the given alphabetic code,
        if it does not already exist.  Return the new or existing town object.
        """
        if not alpha in self.town_map:
            self.town_map[alpha] = Town(alpha)
        return self.town_map[alpha]

    def load_graph(self, infile_name):
        """Load a series of route instructions from the given file."""

        with open(infile_name) as infile_handle:
            for (line_no, line_nl) in enumerate(infile_handle, start=1):
                line = line_nl.rstrip()
                words = re.split(r'\s*, \s*', line)
                for word in words:
                    try:
                        (fm_alpha, to_alpha, distance) = validate_word(word)
                        if fm_alpha == to_alpha:
                            msg = 'route "{0}" doesn\'t go anywhere'
                            raise LoadError(msg.format(word))
                        fm_town = self.add_town(fm_alpha)
                        to_town = self.add_town(to_alpha)
                        fm_town.add_route(to_town, distance, word)
                    except LoadError as error_obj:
                        msg = 'Line {0} [{1}]\n\t{2}'
                        raise LoadError(msg.format(line_no, line, error_obj))

# END Network
#######################################

