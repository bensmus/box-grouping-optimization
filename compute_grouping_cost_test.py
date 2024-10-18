from compute_grouping_cost import compute_group_cost

"""
cells:
 X
 XXX
XXXX
"""
cells = [(2, 0), (0, 1), (1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3)]
group = frozenset({(1, 3), (2, 2)})
assert compute_group_cost(cells, group) == 1, "Wrong group cost"

group = frozenset({(1, 3), (2, 2), (2, 3)}) # Extra group cell does not contribute to group cost.
assert compute_group_cost(cells, group) == 1, "Wrong group cost"

group = frozenset({(2, 0), (1, 2), (2, 2)})
assert compute_group_cost(cells, group) == 0, "Wrong group cost"

"""
cells:
X
XXXX
XXXX
XXXX
"""
cells = [(0, 0)] + [(i, j) for i in range(1, 4) for j in range(4)]
group = frozenset({(3, 0), (3, 1), (3, 2)})
assert compute_group_cost(cells, group) == 7, "Wrong group cost"

"""
cells:
XX
XX
"""
cells = [(i, j) for i in range(2) for j in range(2)]
group = frozenset({(0, 0), (0, 1)})
assert compute_group_cost(cells, group) == 0, "Wrong group cost"