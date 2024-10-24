# import mlrose_hiive as mlrose
from typing import List, Callable, Tuple
from collections import Counter
from compute_grouping_cost import compute_grouping_cost

'''
cells:
XX
XX
XX

grouping:
AA
BC
BC
...expressed as [0, 0, 1, 2, 1, 2]
'''

def get_energy_fn(cells: List[Tuple[int, int]], group_sizes: Counter) -> Callable[[List[int]], float]:
    '''
    Returns a function that evaluates a 1D grouping vector.
    '''

    def correct_group_sizes(state: List[int]) -> bool:
        real_group_sizes = Counter(state)
        return real_group_sizes == group_sizes
    
    def energy(state: List[int]) -> float:
        if not correct_group_sizes(state):
            return float('inf')
        num_groups = len(group_sizes)
        grouping = [[] for _ in range(num_groups)]
        for cell_index, group_index in enumerate(state):
            grouping[group_index].append(cells[cell_index])
        return float(compute_grouping_cost(cells, grouping))
    
    return energy

cells = [(i, j) for i in range(3) for j in range(2)]
energy = get_energy_fn(cells, Counter({0: 2, 1: 2, 2: 2}))
# problem = mlrose.DiscreteOpt(length=6, fitness_fn=energy, maximize=False, max_val=2)
# best_state, lowest_energy = mlrose.hill_climb(problem, max_attempts=10, max_iters=1000, init_state=[0, 0, 1, 1, 2, 2])
# print(best_state)
# print(lowest_energy)

print(energy([0, 0, 1, 1, 2, 2])) # 6
print(energy([0, 0, 1, 2, 1, 2])) # 2
print(energy([0, 0, 1, 2, 2, 2])) # inf