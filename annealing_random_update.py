import random

def random_group_change_inplace(grouping):
    group_count = len(grouping)
    group_size = len(grouping[0])

    random_group_func = lambda: random.randint(0, group_count - 1)
    random_elem_func = lambda: random.randint(0, group_size - 1)

    random_group_1 = random_group_func()
    random_group_2 = random_group_func()
    random_elem_1 = random_elem_func()
    random_elem_2 = random_elem_func()

    old1 = grouping[random_group_1][random_elem_1]
    old2 = grouping[random_group_2][random_elem_2]

    grouping[random_group_1][random_elem_1], grouping[random_group_2][random_elem_2] = old2, old1

if __name__ == '__main__':
    grouping = [[0, 1], [2, 3], [4, 5], [8, 9]]
    random_group_change_inplace(grouping)
    random_group_change_inplace(grouping)
    random_group_change_inplace(grouping)
    random_group_change_inplace(grouping)
    random_group_change_inplace(grouping)
    print(grouping)
