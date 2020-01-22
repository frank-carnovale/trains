
This project is an implementation in Python of the ThoughtWorks "Trains" assignment.

Author
______

Frank Carnovale (frank.carnovale@gmail.com)

Specifications
______________

For specifications and background, please consult ThoughtWorks, Inc.

Algorithm
_________

From the specifications and the expected test results,
it is clear that 'cyclical' trips are allowed, where we define
cyclical trips as *trips in which a town can be departed from more than once*.

This obviously leads to infinitely recurring loops in the solution space of all possible journeys.
These loops see a customer visiting the same city many times in one multi-stop journey.
To contain and simplify this problem, we need to apply a limit on how many stops make up a single
journey.  Without this limit, and with cyclical trips allowed, some abstract queries are 
impractical to solve.

This behaviour can be fine-tuned using constants declared at the top of the ``trains/core.py`` module::

    ALLOW_CYCLICAL_JOURNEYS # boolean. Allows cyclical journeys

    MAXIMUM_STOPS           # integer. Limits stops in multi-stop journeys,
                            #          Only applied when cyclical journeys allowed.

Note that turning off cyclical trips reduces the solution space considerably
and still allows return trips, i.e. trips where a town is both the start-and-end points
of a multi-stop journey.  This is because the town is still only departed from once.

Turning off cyclical-trips reduces the solution space considerably, is more efficient,
and may be considered more sensible by both ticket-issuing officers and customers.
But we currently leave it enabled in order to meet the specifications.

Invocation Methods
__________________

The functionality is implemented in class definitions, so there are various
'wrapper' run-time contexts available, described as follows.

As Stand-alone program
**********************

Usage::

    python trains FILE1 [FILE2..]

    e.g..

    $ python trains tests/data/graph1

    'Trains' Main Program.
    loading tests/data/graph1..
    network has 5 towns

    Q1 Distance of A-B-C is 9

    Q2 Distance of A-D is 5

    Q3 Distance of A-D-C is 13

    Q4 Distance of A-E-B-C-D is 22

    Q5 Distance of A-E-D is NO SUCH ROUTE

    Q6 Routes from C to C with max 3 stops.. 2
            C-E-B-C                 9 km   3 stops
            C-D-C                  16 km   2 stops

    Q7 Routes from A to C with exactly 4 stops.. 3
            A-B-C-D-C              25 km   4 stops
            A-D-C-D-C              29 km   4 stops
            A-D-E-B-C              18 km   4 stops

    Q8 From A to C shortest route.. 9 km
            A-B-C                   9 km   2 stops

    Q9 From B to B shortest route.. 9 km
            B-C-E-B                 9 km   3 stops

    Q10 Routes from C to C under distance 30km.. 7
            C-E-B-C                 9 km   3 stops
            C-E-B-C-E-B-C          18 km   6 stops
            C-E-B-C-E-B-C-E-B-C    27 km   9 stops
            C-E-B-C-D-C            25 km   5 stops
            C-D-C                  16 km   2 stops
            C-D-C-E-B-C            25 km   5 stops
            C-D-E-B-C              21 km   4 stops

    done


The supplied main program (``trains/__main__.py``) will read network definition
files (e.g. ``tests/data/graph1``) from the commandline, then parse and load them.

It will then proceed to run the series of pre-defined queries given in the specifications.

This program can be used as an example to build other client apps using the 'trains' classes.

Test Suite
**********

The supplied test suite will load various good and bad versions of the
network definition files, and will run correctness tests including the entire
query set given in the specifications.  This suite
is suitable for incorporation into a continuous integration subsystem.

It uses **unittest**.

To invoke one of the tests::

    $ python -m tests.test_01load [-v]

To invoke all tests::

    $ python -m unittest discover -v

    # or, to get red-and-green test result colours, if pyrg is available

    $ python -m unittest discover -v |& pyrg

Interactive mode
****************

An interactive mode is available for running the **trains** package
directly under the Python interpreter.  This can be used to experiment with
creation of entire network maps and to invoke queries dynamically.
Any import of the 'trains' package in interactive mode will automatically
cause a menu to be generated.

To work within the 'trains' namespace, a useful approach is to 
start with ``from trains import Network``.  e.g.::

     $ python
     >>> from trains import Network
     Welcome to the Trains package.

     Interactive Mode Usage:
            network = Network()                            Creates a new (empty) network
            network.load_graph(FILE)                       Loads graph information from FILE
     After load_graph()..
            network.towns_count()                          Total towns
            print network.dump()                           Town Routes report
            network.generate_trips()                       Generate all valid trips.
     After generate_trips()..
            network.trips_count()                          Total trips
            network.all_trips()                            Full report of all available trips
            network.distance_of_trip('A-B-C')              Get distance of proposed trip
            trips=network.trips_by_stops('A', 'B', 1, 5)   Show trips from A to B having between 1 and 5 stops
            trips=network.shortest_trip('A', 'B')          Show shortest trip from A to B
            trips=network.trips_in_distance('A', 'B', 20)  Show trips from A to B with total distance under 20

     >>> n = Network()
     >>> n.load_graph('tests/data/graph1')
     >>> print n.towns_count()
     5
     >>> print n.dump()
     TOWN A
     Town A routes out of town are..
             B 5
             E 7
             D 5
     TOWN C
     Town C routes out of town are..
             E 2
             D 8
     TOWN B
     Town B routes out of town are..
             C 4
     TOWN E
     Town E routes out of town are..
             B 3
     TOWN D
     Town D routes out of town are..
             C 8
             E 6
 
     >>> n.generate_trips()
     >>> print n.distance_of_trip('A-B-C')
     9
     >>> print n.shortest_trip('A','B')
     A-B                     5 km   1 stops
     >>> trip = n.shortest_trip('A','B')
     >>> print trip
     A-B                     5 km   1 stops
     >>>
     >>> trips = n.trips_in_distance('C','C',30)
     >>> print len(trips)
     7
     >>> for t in trips:
     ...     print t
     ...
     C-E-B-C                 9 km   3 stops
     C-E-B-C-E-B-C          18 km   6 stops
     C-E-B-C-E-B-C-E-B-C    27 km   9 stops
     C-E-B-C-D-C            25 km   5 stops
     C-D-C                  16 km   2 stops
     C-D-C-E-B-C            25 km   5 stops
     C-D-E-B-C              21 km   4 stops
     >>>
 
     ... and so on.
 
Style Convention
________________

Application code in the `trains` package is lint-checked using basic 'pylint'.
Lint options are mostly defaulted except for some minor gray-area issues.  
See the pylintrc file is in the project root directory for non-default settings.

The test modules use some particular layout techniques and are not lint-friendly.

