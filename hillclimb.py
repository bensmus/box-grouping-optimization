def hillclimb(state, random_move_func, energy_func, step_count_max, step_tries_max):
    def hillclimb_iteration(state):
        energy = energy_func(state)
        for _ in range(step_tries_max):
            random_state = random_move_func(state)
            random_state_energy = energy_func(random_state)
            if random_state_energy < energy:
                return random_state, random_state_energy, False
        return state, energy, True
    for _ in range(step_count_max):
        state, energy, done = hillclimb_iteration(state)
        if done:
            return state, energy, True # FIXME
    return state, energy, False

if __name__ == '__main__':
    import random
    def set_random_bit(state):
        random_bit = random.randint(0, len(state) - 1)
        return state[:random_bit] + [random.randint(0, 1)] + state[random_bit+1:]
    def energy_func(state):
        return state[0] - state[1] + state[3]
    state = [1, 1, 1, 1, 1]
    state, energy, reached_local_minima = hillclimb(state, set_random_bit, energy_func, 3, 1) # FIXME
    print(state, energy, reached_local_minima)

# reached_local_minima is not true