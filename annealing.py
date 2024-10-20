from simanneal import Annealer
from annealing_random_update import random_group_change_inplace
from compute_grouping_cost import compute_grouping_cost
import random

def random_initial_grouping(cells, group_size):
    grouping = []
    group_count = len(cells) // group_size
    cells_shuffled = random.sample(cells, len(cells))
    for _ in range(group_count):
        group = []
        for _ in range(group_size):
            group.append(cells_shuffled.pop())
        grouping.append(group)
    return grouping

cells = [(i, j) for i in range(3) for j in range(2)]

class WarehouseOptimizer(Annealer):
    def __init__(self, cells, group_size):
        self.cells = cells
        self.state = random_initial_grouping(self.cells, group_size)
        super(WarehouseOptimizer, self).__init__(self.state)
    def move(self):
        random_group_change_inplace(self.state)
    def energy(self):
        return compute_grouping_cost(self.cells, self.state)

def print_grouping(cells, grouping):
    def get_which_group(cell, grouping):
        """Returns which group the cell is part of."""
        for i, group in enumerate(grouping):
            if cell in group:
                return i
        return None # No grouping
    rows = [row for (row, _) in cells]
    cols = [col for (_, col) in cells]
    for row in range(max(rows) + 1):
        for col in range(max(cols) + 1):
            iter_cell = (row, col)
            which_group = get_which_group(iter_cell, grouping)
            if which_group == None:
                print(' ', end='')
            else:
                print(which_group, end='')
        print()

optimizer = WarehouseOptimizer(cells, 2)
state, energy = optimizer.anneal()
print() # Fixes linanneal print bug.
print(state)
print_grouping(cells, state)

'''
Decent results for state. Either gives
AA
BC
BC --- optimal

AB
CB
CA --- ok

AB
AB
CC --- ok
'''