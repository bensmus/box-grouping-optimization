import random
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colormaps
from simanneal import Annealer


def random_group_change_inplace(grouping):
    random_index_func = lambda l: random.randint(0, len(l) - 1)
    random_group_1 = random_index_func(grouping)
    random_group_2 = random_index_func(grouping)
    random_elem_1 = random_index_func(grouping[random_group_1])
    random_elem_2 = random_index_func(grouping[random_group_2])
    old1 = grouping[random_group_1][random_elem_1]
    old2 = grouping[random_group_2][random_elem_2]
    grouping[random_group_1][random_elem_1], grouping[random_group_2][random_elem_2] = old2, old1


def greedy_cell_assign(cells, group_sizes):
    '''
    Find the cells that should be assigned to the group based on heuristic
    of vertically-aligned cells in hard-to-access location.

    If cells cannot fully vertically fit, then split into groups and fit them.
    '''

    def pop_from_cells_remaining(cells_remaining, group_size):
        '''
        HEURISTIC IS IMPLEMENTED HERE.

        Look at the number of rows for each column in cells_remaining.
        (Because of the assignment scheme, cells_remaining will always have
        vertically contiguous cells.)
        Then pop the bottom-most cells from the column with the largest number of rows.
        '''

        column_to_rows = [] # Match each column to its rows.
        columns = {column for (_, column) in cells_remaining}
        for column in columns:
            rows = [row for (row, _) in filter(lambda cell: cell[1] == column, cells_remaining)]
            column_to_rows.append((column, rows))
        
        target_column, target_rows = max(column_to_rows, key=lambda pair: len(pair[1])) # The column with the most rows.
        target_rows.sort(reverse=True)
        num_cells_found = min(group_size, len(target_rows)) # How many cells we're popping.
        group_size_remaining = group_size - num_cells_found
        found_cells = [(row, target_column) for row in target_rows[:num_cells_found]] # The bottom cells from a column.
        for found_cell in found_cells:
            cells_remaining.remove(found_cell)
        return found_cells, group_size_remaining

    groups_remaining = [] # Queue of (group_size, group_index) to be grouped.
    for group_index, group_size in enumerate(group_sizes):
        groups_remaining.append((group_size, group_index))
    
    cells_remaining = copy.deepcopy(cells)
    grouping = [[] for _ in group_sizes]

    while groups_remaining != []:
        # Deal with large group first, vertical bottom-most cells to it (found_cells).
        group_size, group_index = max(groups_remaining)
        groups_remaining.remove((group_size, group_index))
        found_cells, group_size_remaining = pop_from_cells_remaining(cells_remaining, group_size)
        grouping[group_index].extend(found_cells)
        if group_size_remaining != 0: # Did not find vertically contiguous big enough.
            groups_remaining.append((group_size_remaining, group_index))
    return grouping


def compute_grouping_cost(cells, grouping):
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
    """
    E.g. 3x2 stack:
    cells = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    grouping = { {(0, 0), (0, 1)}, {(1, 0), (1, 1)}, {(2, 0), (2, 1)} }
    grouping_cost would be 2 because avg of first group cost is 0, second is 2, third is 4.
    """
    group_costs = [compute_group_cost(cells, group) for group in grouping]
    grouping_cost = sum(group_costs)
    return grouping_cost


class MyAnnealer(Annealer):
    def __init__(self, cells, group_sizes):
        self.cells = cells
        self.state = greedy_cell_assign(self.cells, group_sizes)
        self.Tmax = 0.001
        self.Tmin = 0.001
        super(MyAnnealer, self).__init__(self.state)

    def move(self):
        random_group_change_inplace(self.state)

    def energy(self):
        return compute_grouping_cost(self.cells, self.state)
    

def compute_optimal_grouping(cells, group_sizes):
    # GREEDY AND HILLCLIMB # FIXME is hillclimb good enough??

    # Also make a more elegant function: add method arg and then
    # always run greedy first and then annealer or hillclimb.

    annealer = MyAnnealer(cells, group_sizes)
    grouping, energy = annealer.anneal()

    # JUST GREEDY
    # grouping = greedy_cell_assign(cells, group_sizes)
    # energy = compute_grouping_cost(cells, grouping)
    return grouping, energy


def draw_grouping(cells, grouping):
    def get_which_group(cell, grouping):
        """Returns which group the cell is part of."""
        for i, group in enumerate(grouping):
            if cell in group:
                return i
    _, ax = plt.subplots()
    colors = colormaps['tab20']
    cell_rows = [row for (row, _) in cells]
    num_rows = max(cell_rows) + 1
    for cell in cells:
        group = get_which_group(cell, grouping)
        rect = patches.Rectangle((cell[1], num_rows - cell[0] - 1), 1, 1, facecolor=colors(group), edgecolor='black')
        ax.add_patch(rect)
    ax.set_xlim(0, 20) # FIXME
    ax.set_ylim(0, 20) # FIXME
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


'''
 XXXX
XXXXX
XXXXX
'''
# cells = [(0, j) for j in range(1, 5)] + [(i, j) for i in range(1, 3) for j in range(5)]
# group_sizes = [4, 2, 2, 3, 3]

'''
XXXX
XXXX
XXXX
'''
# cells = [(i, j) for i in range(3) for j in range(4)]
# group_sizes = [2] * 6

'''
XXXXX
XXXXX
XXXXX
XXXXX
'''
cells = [(i, j) for i in range(4) for j in range(5)]
group_sizes = [5] * 4

# Big test! 100 printers!
# cells = [(i, j) for i in range(10) for j in range(10)]
# group_sizes = [5] * 10 + [20] + [6] * 5

# 100 printers in non-square formation:
# cells = [(i, j) for i in range(10) for j in range(5)] + [(i, j) for i in range(10, 15) for j in range(10)]
# group_sizes = [5] * 10 + [20] + [6] * 5

print(cells)
grouping, energy = compute_optimal_grouping(cells, group_sizes)
print()
print('energy:', energy)
draw_grouping(cells, grouping)