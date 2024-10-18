import itertools
from compute_grouping_cost import compute_grouping_cost

def exclude(ar, elems):
    return [elem for elem in ar if elem not in elems]

def compute_all_groupings(ar, group_size):
    """
    A grouping is defined as a subdivision of `ar` into groups where
    all of the groups have size `group_size`. So if `ar` is [A, B, C, D, E, F],
    one possible grouping with `group_size` 3 would be { {A, B, E}, {C, D, F} }.
    """
    # Use a set to ensure that all the groupings are unique.
    groupings = set()
    # A recursive function that updates groupings.
    # `accumulated` is the current labeling, `remaining` is what remains to be labeled.
    def recursive(accumulated, remaining):
        for pair in itertools.combinations(remaining, group_size):
            next_accumulated = accumulated.union({frozenset(pair)}) # `next_accumulated` is a set of frozensets.
            next_remaining = exclude(remaining, pair)
            if next_remaining == []: # We fully divided the printers up.
                groupings.add(frozenset(next_accumulated)) # Sets aren't hashable, so frozenset it.
            recursive(next_accumulated, next_remaining)
    recursive(set(), ar)
    return groupings

def compute_best_groupings(cells, grouping_size):
    groupings = list(compute_all_groupings(cells, grouping_size)) # list() For consistent iteration.
    grouping_costs = []
    for grouping in groupings:
        grouping_costs.append(compute_grouping_cost(cells, grouping))
    best_groupings = [grouping for i, grouping in enumerate(groupings) if grouping_costs[i] == min(grouping_costs)]
    print(min(grouping_costs))
    return best_groupings

"""
Groups of 3 for:
XX
XXXX
XXXXXX
"""
# Runs in 3 seconds.
# cells = [(0, j) for j in range(2)] + [(1, j) for j in range(4)] + [(2, j) for j in range(6)]
# print(compute_best_groupings(cells, 3))

"""
Finds 2:

AB
ABCD
ABCDCD

and

AB
ABCD
ABCDDC

which both have 0 cost.
"""

"""
Groups of 3 for:
XX
XXXX
XXXX
XXXX
XXXX
"""
# Does not complete in 1.5 hours.
# cells = [(0, 0), (0, 1)] + [(i, j) for i in range(1, 5) for j in range(4)]
# print(compute_best_groupings(cells, 3))

# Runs in 272 seconds.
# compute_all_groupings(list(range(15)), 3)