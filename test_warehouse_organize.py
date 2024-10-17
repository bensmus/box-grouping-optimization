from warehouse_organize import compute_group_cost

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