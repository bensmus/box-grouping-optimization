from simanneal import Annealer
from annealing_random_update import random_group_change_inplace
from compute_grouping_cost import compute_grouping_cost

cells = [(i, j) for i in range(3) for j in range(2)]

class WarehouseOptimizer(Annealer):
    def move(self):
        random_group_change_inplace(self.state)
    def energy(self):
        return compute_grouping_cost(cells, self.state)

optimizer = WarehouseOptimizer([[(0, 0), (0, 1)], [(1, 0), (1, 1)], [(2, 0), (2, 1)]])
state, energy = optimizer.anneal()
print(state)

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