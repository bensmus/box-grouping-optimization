def compute_group_cost(cells, group):
    # `cells` and `group` are both collections of tuples.
    cell_rows = [row for (row, _) in cells]
    cells_height = max(cell_rows) - min(cell_rows) + 1
    group_cost = 0
    # Iterate through a bounding box of cells,
    # simulating the access of group (from top to bottom).
    group_columns = {column for (_, column) in group} # Set ensures that same column not scanned twice.
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