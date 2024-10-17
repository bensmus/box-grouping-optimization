import itertools

def exclude(ar, elems):
    return [elem for elem in ar if elem not in elems]

def compute_all_groupings(ar, group_size):
    """
    compute_all_groupings([1, 2, 3, 4], 2) gives [{{2, 4}, {1, 3}}, {{1, 4}, {2, 3}}, {{3, 4}, {1, 2}}]
    but all the sets are frozensets.
    """
    # Use a set to ensure that all the partitions are unique.
    partitions = set()
    # A recursive function that updates partitions.
    # `accumulated` is the current labeling, `remaining` is what remains to be labeled.
    def recursive(accumulated, remaining):
        for pair in itertools.combinations(remaining, group_size):
            next_accumulated = accumulated.union({frozenset(pair)}) # `next_accumulated` is a set of frozensets.
            next_remaining = exclude(remaining, pair)
            if next_remaining == []: # We fully divided the printers up.
                partitions.add(frozenset(next_accumulated)) # Sets aren't hashable, so frozenset it.
            recursive(next_accumulated, next_remaining)
    recursive(set(), ar)
    return list(partitions) # For consistent iteration.

def compute_group_cost(cells, group):
    # `cells` and `group` are both collections of tuples.
    cell_rows = [row for (row, _) in cells]
    cells_height = max(cell_rows) - min(cell_rows) + 1
    group_cost = 0
    # Iterate through a bounding box of cells,
    # simulating the access of group (from top to bottom).
    group_columns = [column for (_, column) in group]
    for column in group_columns:
        column_subcosts = []
        cell_above_flag = False
        cells_above = 0 # Important for non-rectangular cell stacks.
        for row in range(cells_height):
            iter_cell = (row, column)
            if iter_cell in group:
                if not cell_above_flag: # Consider whether cell above was in group.
                    column_subcosts.append(cells_above)
                cell_above_flag = True
            else:
                cell_above_flag = False
            if iter_cell in cells:
                cells_above += 1
        column_cost = sum(column_subcosts)
        group_cost += column_cost
    return group_cost

def compute_grouping_cost(cells, grouping):
    """
    E.g. 3x2 stack:
    cells = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    grouping = { {(0, 0), (0, 1)}, {(1, 0), (1, 1)}, {(2, 0), (2, 1)} }
    grouping_cost would be 2 because avg of first group cost is 0, second is 2, third is 4.
    """
    group_costs = [compute_group_cost(cells, group) for group in grouping]
    grouping_cost = sum(group_costs) / len(group_costs) # Average group cost.
    return grouping_cost

def compute_best_groupings(cells, grouping_size):
    groupings = compute_all_groupings(cells, grouping_size)
    grouping_costs = []
    for grouping in groupings:
        grouping_costs.append(compute_grouping_cost(cells, grouping))
    best_groupings = [grouping for i, grouping in enumerate(groupings) if grouping_costs[i] == min(grouping_costs)]
    return best_groupings

"""
Groups of 3 for:
XX
XXXX
XXXXXX
"""
