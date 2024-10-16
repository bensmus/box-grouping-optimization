import itertools

def exclude(ar, elems):
    return [elem for elem in ar if elem not in elems]

def compute_all_groupings(ar, group_size):
    '''
    compute_all_groupings([1, 2, 3, 4], 2) gives [{{2, 4}, {1, 3}}, {{1, 4}, {2, 3}}, {{3, 4}, {1, 2}}]
    but all the sets are frozensets.
    '''
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

# Cells are (row, col) tuples.
def is_vertically_adjacent(cell_pair):
    cell_a, cell_b = cell_pair
    is_close_rows = abs(cell_a[0] - cell_b[0]) == 1
    is_same_col = cell_a[1] == cell_b[1]
    return is_close_rows and is_same_col

def compute_grouping_score(grouping):
    def compute_group_score(group):
        # group could be frozenset({(1, 2), (3, 4)})
        # TODO: Verify correctness of 2 lines below.
        group_height = max([row for (row, _) in group])
        group_by_column = list(sorted(group, key=lambda cell: cell[1] * group_height + cell[0]))
        print(group_by_column)
        return 1
    group_scores = [compute_group_score(group) for group in grouping]
    return sum(group_scores) / len(group_scores)

def compute_best_groupings(cells, grouping_size):
    groupings = compute_all_groupings(cells, grouping_size)
    grouping_scores = []
    for grouping in groupings:
        grouping_scores.append(compute_grouping_score(grouping))
    best_score = min(grouping_scores)
    best_groupings = [grouping for i, grouping in enumerate(groupings) if grouping_scores[i] == best_score]
    return best_groupings

# print(compute_best_groupings([(i, j) for i in range(3) for j in range(4)], 2))

"""
Groups of 3 for:
XX
XXXX
XXXXXX
"""

# cells = [(i, j) for i in range(1, 3) for j in range(4)] + [(0, 0), (0, 1)] + [(2, 4), (2, 5)]
# print(compute_best_groupings(cells, 3))

compute_grouping_score(compute_all_groupings([(1, 2), (2, 3), (0, 1), (4, 5), (4, 6), (4, 2)], 3)[0])