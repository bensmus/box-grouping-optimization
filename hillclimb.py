def hillclimb(state, random_move_func, fitness_func, tries_per_step, maximize=True):
    """
    Hillclimbs until reaches state that is likely a local minima,
    since after `tries_per_step` of applying `random_move_func` to `state`, no lower energy state was found.
    """
    def hillclimb_iteration(state):
        fitness = fitness_func(state)
        continue_hillcimbing = True
        sign = 1 if maximize else -1
        print(state, fitness)
        for _ in range(tries_per_step):
            random_state = random_move_func(state)
            random_state_fitness = fitness_func(random_state)
            if sign * random_state_fitness > sign * fitness:
                return random_state, random_state_fitness, continue_hillcimbing
        return state, fitness, not continue_hillcimbing
    steps_completed = 0
    while True:
        state, fitness, continue_hillcimbing = hillclimb_iteration(state)
        steps_completed += 1
        if not continue_hillcimbing:
            return state, fitness, steps_completed

if __name__ == '__main__':
    import random
    import copy
    '''
    def set_random_bit(state):
        random_bit = random.randint(0, len(state) - 1)
        return state[:random_bit] + [random.randint(0, 1)] + state[random_bit+1:]
    def energy_func(state):
        return state[0] - state[1] + state[3]
    state = [0, 1, 1, 0, 1]
    state, energy, steps_completed = hillclimb(state, set_random_bit, energy_func, 100)
    print(state, energy, steps_completed)
    '''

    from grouping_random import random_initial_grouping, random_group_change_inplace, print_grouping
    from compute_grouping_cost import compute_grouping_cost
    def random_move_func(state):
        state2 = copy.deepcopy(state) # Deepcopy is necessary to avoid modifying state.
        random_group_change_inplace(state2)
        return state2
    '''
       XX
      XXX
     XXXX
     XXXX
    XXXXX
    '''
    cells = [
        (0, 3), (0, 4),
        (1, 2), (1, 3), (1, 4),
        (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)
    ]
    state = random_initial_grouping(cells, 3)
    def energy_func(state):
        return compute_grouping_cost(cells, state)
    best_state, best_energy, steps_completed = hillclimb(state, random_move_func, energy_func, 1000, maximize=False)
    print_grouping(cells, best_state)
    print(best_energy)
