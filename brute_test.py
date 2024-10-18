from brute import compute_all_groupings

assert compute_all_groupings([1, 2, 3, 4], 2) == {
    frozenset({
        frozenset({1, 2}), frozenset({3, 4})
    }),
    frozenset({
        frozenset({1, 3}), frozenset({2, 4})
    }),
    frozenset({
        frozenset({1, 4}), frozenset({2, 3})
    })
}
