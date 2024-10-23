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

class WarehouseOptimizer(Annealer):
    def __init__(self, cells, group_size):
        self.Tmin = 0.0001
        self.Tmax = 0.0001
        self.steps = 1000
        self.cells = cells
        self.state = random_initial_grouping(self.cells, group_size)
        super(WarehouseOptimizer, self).__init__(self.state)
    def move(self):
        random_group_change_inplace(self.state)
    def energy(self):
        return compute_grouping_cost(self.cells, self.state)

def print_grouping(cells, grouping):
    def get_which_group(cell, grouping):
        def alpha_from_index(index):
            return chr(ord('A') + index)
        """Returns which group the cell is part of."""
        for i, group in enumerate(grouping):
            if cell in group:
                return alpha_from_index(i)
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

def run_annealing(cells, group_size):
    optimizer = WarehouseOptimizer(cells, group_size)
    state, energy = optimizer.anneal()
    print()
    print_grouping(cells, state)
    print('Energy:', energy)
    print('--------')
    return state, energy

def compute_best_state(cells, group_size, num_iter):
    assert num_iter > 0, "num_iter must be greater than zero"
    best_state, best_energy = run_annealing(cells, group_size)
    for i in range(num_iter - 1): # Already ran once.
        print(f'Iter #{i}')
        state, energy = run_annealing(cells, group_size)
        if energy < best_energy:
            best_state = state
            best_energy = energy
    return best_state, best_energy

'''
cells:
XX
XX
XX
'''
# cells = [(i, j) for i in range(3) for j in range(2)]
# run_annealing(cells, 2)

'''
cells:
XX
XXXX
XXXX
XXXX
XXXX
'''
cells = [(0, 0), (0, 1)] + [(i, j) for i in range(1, 5) for j in range(4)]
best_state, best_energy = compute_best_state(cells, 3, 10)
print(f'Best state (energy {best_energy}):')
print_grouping(cells, best_state)

'''
DEFAULTS:
Tmax = 25000.0  # Max (starting) temperature
Tmin = 2.5      # Min (ending) temperature
steps = 50_000   # Number of iterations
updates = 100   # Number of updates (by default an update prints to stdout)

RESULTS OF `optimizer.auto`:
steps = 2_600_000
Tmax = 48.0

...So the problem is biased to a large number of low temperature steps.
'''

# TODO

# Show how large of an impact changing Tmax and Tmin had: consitent lowest energy state!
# Why was copy strategy 'slice' disastrous?