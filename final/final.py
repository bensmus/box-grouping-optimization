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
    group_sizes_cpy = list(group_sizes)
    cells_remaining = copy.deepcopy(cells)
    grouping = []
    for group_size in group_sizes:
        ... # FIXME
    return grouping

def get_initial_grouping(cells, group_sizes):
    assert sum(group_sizes) == len(cells), f'Invalid group_sizes given cells has {len(cells)} elements'
    grouping = []
    current_cell = 0
    for size in group_sizes:
        group = []
        for _ in range(size):
            cell = cells[current_cell]
            group.append(cell)
            current_cell += 1
        grouping.append(group)
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
        self.state = get_initial_grouping(self.cells, group_sizes)
        self.Tmax = 100
        self.Tmin = 0.001
        super(MyAnnealer, self).__init__(self.state)
    def move(self):
        random_group_change_inplace(self.state)
    def energy(self):
        return compute_grouping_cost(self.cells, self.state)
    
def compute_optimal_grouping(cells, group_sizes):
    annealer = MyAnnealer(cells, group_sizes)
    grouping, energy = annealer.anneal()
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
grouping, energy = compute_optimal_grouping(cells, group_sizes, True)
print()
print('energy:', energy)
draw_grouping(cells, grouping)