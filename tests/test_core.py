import sys
import os
import pytest
from copy import deepcopy
from typing import Optional, Tuple
from collections import Counter

# Moves up a level from the test file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cnf import CNF
from core.dpll import DPLL
from core.sudoku import Sudoku

# ---------
# Test CNF
# ---------


@pytest.mark.parametrize("variable, assignment, expected", [
    (-4, True, False),
    (4, True, True),
    (4, False, False),
    (-4, False, True),
    (-4, None, None),
    (4, None, None),
])
def test_evaluate_var(variable: int, assignment: Optional[bool], expected: Optional[bool]):
    result = CNF.evaluate_var(variable, assignment)
    assert result is expected


@pytest.mark.parametrize("clause, list_var, expected", [
    ([1, -2, 3, -4], [True, True, False, None], True),
    ([1, -2, 3, -4], [False, True, False, None], None),
    ([1, -2, 3, -4], [None, True, False, True], None),
    ([1, -3], [False, False, True], False),
    ([], [False, False, True], False),
    ([1, 2, 3], [False, False, True], True),
])
def test_evaluate_clause(clause: list[int], list_var: list[Optional[bool]], expected: Optional[bool]):
    result = CNF.evaluate_clause(clause, list_var)
    assert result is expected


@pytest.mark.parametrize("list_var, expected", [
    ([True, False, False, None], True),
    ([None, False, False, None], None),
    ([True, False, True, False], False),
])
def test_evaluate(list_var: list[Optional[bool]], expected: Optional[bool]):
    cnf = CNF([[1, 2], [2, -3, 4], [-1, -2], [-1, -2, -3], [1]], list_var)
    cnf.evaluate()
    assert cnf.get_satisfiable() is expected


@pytest.mark.parametrize("literal, expected, value", [
    (4, [[-1, 2, 3], [-1, -2, -5], []], True),
    (-5, [[-1, 2, 3, -4], [-3, 4], [-2, 3, 4], [-4]], False),
])
def test_remove_litt(literal: int, expected: list[list[int]], value: bool):
    cnf = CNF([[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4]], [None] * 5)
    cnf.remove_literal(literal)
    assert cnf.get_actual_cnf() == expected
    assert cnf.get_list_var()[abs(literal)-1] is value
    assert cnf.get_history().__contains__((abs(literal)-1, value))


@pytest.mark.parametrize("formula, list_var, expected", [
    ([[-5, -3, 4, -1], [3], [5, -2], [-2, 1, -4], [1, -3]], [False, None, None, False, None], [[3], [5, -2], [-3]]),
    ([[3, 2, 1], [-1, -2, 5]], [False, True, False, True, False], []),
    ([[-5, -1], [-1, -3], [4], [-4, 1], [-2, -1, 3]], [None, None, None, True, None], [[-5, -1], [-1, -3], [1], [-2, -1, 3]])
])
def test_init(formula: list[list[int]], list_var: list[Optional[bool]], expected: list[list[int]]):
    cnf = CNF(formula, list_var)
    assert cnf.get_initial_cnf() == expected
    assert cnf.get_actual_cnf() == expected
    assert cnf.get_list_var() == list_var
    assert cnf.get_history() == []


@pytest.mark.parametrize("changes, expected", [
    ([(0, True), (1, True), (2, False)], [[-5], [4, 5], [-4, 5]]),
    ([(0, True), (1, True), (2, False), (3, True), (4, False)], [[]]),
    ([(0, True), (1, True), (2, False), (3, False)], [[-5], [5]])
])
def test_restore_state(changes: list[Tuple[int, bool]], expected: list[list[int]]):
    cnf = CNF([[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]], [None] * 5)
    cnf.restore_state(changes)
    assert cnf.get_actual_cnf() == expected
    assert cnf.get_history() == changes
    assert cnf.get_initial_cnf() == [[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]]


# ---------
# Test DPLL
# ---------


@pytest.mark.parametrize("formula, variables, history, simplifications, oracle_formula, oracle_vars, oracle_history, oracle_simpl", [
    (
        [[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]],
        [True, True, False, True, False],
        [[0, True], [1, True], [2, False], [4, False], [3, True]],
        [4, 3],
        [[3, -4], [-3, 4, 5], [-4, 5]],
        [True, False, None, None, None],
        [(0, True), (1, False)],
        []
    ),
    (
        [[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]],
        [True, True, True, True, False],
        [[0, True], [1, True], [2, True], [3, True], [4, False]],
        [],
        [[-5], [5]],
        [True, True, True, False, None],
        [(0, True), (1, True), (2, True), (3, False)],
        []
    ),
    (
        [[3, 1], [1], [-2, 3, -5], [-1, 3], [-4, -3, -2]],
        [True, None, False, None, True],
        [[0, True]],
        [0],
        [[3, 1], [1], [-2, 3, -5], [-1, 3], [-4, -3, -2]],
        [None, None, None, None, None],
        [],
        []
    )
])
def test_back(formula, variables, history: list[Tuple[int, bool]], simplifications, oracle_formula, oracle_vars, oracle_history: list[Tuple[int, bool]], oracle_simpl):
    dpll = DPLL(CNF(deepcopy(formula), [None] * len(variables)))
    dpll._DPLL__list_simplifications = simplifications[:]
    dpll._DPLL__formula.restore_state(history)
    dpll._DPLL__back()
    res_cnf = dpll._DPLL__formula
    assert res_cnf.get_actual_cnf() == oracle_formula
    assert res_cnf.get_list_var() == oracle_vars
    assert res_cnf.get_history() == oracle_history
    assert dpll._DPLL__list_simplifications == oracle_simpl


@pytest.mark.parametrize("formula, variables, history, simplifications, oracle_formula, oracle_vars, oracle_history, oracle_simpl", [
    (
        [[-5], [4, 5], [-4, 5]],
        [True, True, False, None, None],
        [(0, True), (1, True), (2, False)],
        [],
        [[4], [-4]],
        [True, True, False, None, False],
        [(0, True), (1, True), (2, False), (4, False)],
        [4]
    ),
    (
        [[-5, 4], [2, 4, 5], [-2, 5]],
        [True, None, None, None, None],
        [(0, True)],
        [0],
        [[-2, 5]],
        [True, None, None, True, None],
        [(0, True), (3, True)],
        [0, 3]
    ),
    (
        [[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]],
        [None, None, None, None, None],
        [],
        [],
        [[-1, 2, 3], [-1, -2, -5], [5]],
        [None, None, None, True, None],
        [(3, True)],
        []
    ),
    (
        [[4, 5], [-4, 5]],
        [True, False, True, None, None],
        [(0, True), (1, False), (2, True)],
        [],
        [],
        [True, False, True, None, True],
        [(0, True), (1, False), (2, True), (4, True)],
        [4]
    )
])
def test_progress(formula, variables, history: list[Tuple[int, bool]], simplifications, oracle_formula, oracle_vars, oracle_history: list[Tuple[int, bool]], oracle_simpl):
    dpll = DPLL(CNF(deepcopy(formula), [None] * len(variables)))
    dpll._DPLL__formula.set_state(None, None, variables, variables, history)
    dpll._DPLL__list_simplifications = simplifications[:]
    dpll._DPLL__progress()
    res_cnf = dpll._DPLL__formula
    assert res_cnf.get_actual_cnf() == oracle_formula
    assert res_cnf.get_list_var() == oracle_vars
    assert res_cnf.get_history() == oracle_history
    assert dpll._DPLL__list_simplifications == oracle_simpl


@pytest.mark.parametrize("formula_init, formula_actual, variables, history, simplifications, oracle_res, oracle_vars", [
    (
        [[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]],
        [[2, 3, -4], [-2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]],
        [True, None, None, None, None],
        [(0, True)],
        [],
        True,
        [True, False, True, True, True]
    ),
    (
        [[1, 2, 4, -5], [-1, 2, 3, -4], [-1, -2, -5], [-3, 4, 5], [-2, 3, 4, 5], [-4, 5]],
        [[3, -4]],
        [True, False, None, None, True],
        [(0, True), (1, False), (4, True)],
        [4],
        True,
        [True, False, True, None, True]
    ),
    (
        [[-5, 2, -3, -4], [1, -5], [5, 2], [3, -2, 4], [5, -2, -1]],
        [[2], [-2, 4]],
        [False, None, False, None, False],
        [(4, False)],
        [4],
        True,
        [False, True, False, True, False]
    ),
    (
        [[5], [3, -5, -1, -2], [1, -2, -5], [2, -5, 1, -3], [3]],
        [[-2], [2, -3], [3]],
        [False, None, None, False, True],
        [(4, True)],
        [4],
        False,
        [False, None, None, False, True]
    ),
])
def test_solve(formula_init, formula_actual, variables, history, simplifications, oracle_res, oracle_vars):
    dpll = DPLL(CNF(deepcopy(formula_init), [None] * len(variables)))
    dpll._DPLL__formula.set_state(formula_init, formula_actual, variables, variables, history)
    dpll._DPLL__list_simplifications = simplifications[:]
    res = dpll.solve()
    assert res == oracle_res
    assert dpll._DPLL__formula.get_list_var() == oracle_vars


# ---------
# Test Sudoku
# ---------


def test_init_list_var():
    expected = [False, True, False, False, None, None, None, None, False, False, True, False, None, None, None, None,
                None, None, None, None, True, False, False, False, None, None, None, None, False, True, False, False,
                None, None, None, None, None, None, None, None, False, True, False, False, False, False, False, True,
                False, False, False, True, False, True, False, False, None, None, None, None, None, None, None, None]
    sudoku = Sudoku(2)
    sudoku.add((0, 0, 2))
    sudoku.add((2, 0, 3))
    sudoku.add((1, 1, 1))
    sudoku.add((3, 1, 2))
    sudoku.add((2, 2, 2))
    sudoku.add((3, 2, 4))
    sudoku.add((0, 3, 4))
    sudoku.add((1, 3, 2))
    assert sudoku._Sudoku__init_list_var() == expected


def test_set_grid_from_var():
    lv = [False, False, False, False, False, False, False, False, True, False, False, True, False, False, False,
                False, False, False, False, True, False, False, False, False, False, False, False, False, False, False,
                False, False, True, False, False, False, True, False, False, False, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, False, False, False, True, False, False,
                False, False, False, False, False, False, False, False, False, True, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, False, True, False, False, False, False,
                False, False, False, False, False, False, False, True, False, False, False, False, False, False, True,
                False, False, False, False, True, False, False, False, False, False, False, False, False, False, False,
                True, False, False, False, False, False, False, False, False, False, False, False, True, False, False,
                True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False, True, False, False, True, False, False, False, False, False, False, True, False, False,
                False, False, False, False, False, False, False, False, False, False, False, False, True, False, False,
                False, False, False, True, False, False, False, False, False, False, False, True, False, False, False,
                False, False, False, False, False, False, False, False, False, False, True, False, False, False, False,
                False, False, False, False, False, True, False, True, False, False, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, False, False, False, False, False, True,
                False, False, False, False, False, False, False, False, True, False, False, False, False, False, False,
                False, False, False, False, False, True, True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, True, False, False, False, False, False, True, False,
                False, False, False, False, False, False, True, False, False, False, False, False, False, False, False,
                False, False, False, True, False, False, False, False, True, False, False, False, False, False, False,
                False, True, False, False, False, False, False, False, False, False, False, False, False, False, False,
                True, False, False, False, True, False, False, False, False, False, False, False, False, False, False,
                False, True, False, False, False, False, True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, True, False, False, False, False, False, True, False, False, False,
                False, False, False, False, False, False, False, False, False, False, False, True, False, False, False,
                False, False, False, False, True, False, False, False, False, True, False, False, False, False, False,
                False, False, False, False, False, False, False, True, False, False, False, False, True, False, False,
                False, False, False, False, False, True, False, False, False, False, False, False, False, False, False,
                False, False, False, True, False, False, False, False, False, False, False, False, False, False, True,
                False, True, False, False, False, False, False, False, False, False, False, False, False, True, False,
                False, False, False, False, False, False, False, False, True, False, False, False, True, False, False,
                False, False, False, False, False, False, False, False, True, False, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, False, False, False, False, False, False,
                False, False, True, False, False, False, True, False, False, False, False, False, False, True, False,
                False, False, False, False, False, False, False, False, False, False, False, False, False, True, False,
                False, False, False, False, False, True, False, False, False, True, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False, True, False, False, False, False, False,
                True, False, False, False, False, False, False, False, False, False, False, True, False, False, False,
                False, False, False, False, False, False, False, True, False, False, False, False, False, True, False,
                False, False, False, False, False, False, False, False, False, True, False, False, True, False, False,
                False, False, False, False, False, False, False, False, True, False, False, False, False, False, False,
                False, True, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False, True, False, True, False, False, False, False, False, False, False, True, False, False,
                False, False, False, False, False, False, False, False, False, False, False, False, True, False, False,
                False, False, False, False, False, False, False, False, True, False, False, True, False, False, False,
                False, False, False, False, False, False, False, False, True, False, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, True, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False]
    expected = [
        (0, 0, 9), (1, 0, 3), (2, 0, 2), (3, 0, 6), (4, 0, 1), (5, 0, 5), (6, 0, 4), (7, 0, 7), (8, 0, 8),
        (0, 1, 5), (1, 1, 8), (2, 1, 6), (3, 1, 2), (4, 1, 4), (5, 1, 7), (6, 1, 1), (7, 1, 9), (8, 1, 3),
        (0, 2, 1), (1, 2, 7), (2, 2, 4), (3, 2, 3), (4, 2, 8), (5, 2, 9), (6, 2, 2), (7, 2, 5), (8, 2, 6),
        (0, 3, 6), (1, 3, 9), (2, 3, 1), (3, 3, 8), (4, 3, 5), (5, 3, 4), (6, 3, 7), (7, 3, 3), (8, 3, 2),
        (0, 4, 7), (1, 4, 2), (2, 4, 5), (3, 4, 1), (4, 4, 6), (5, 4, 3), (6, 4, 9), (7, 4, 8), (8, 4, 4),
        (0, 5, 8), (1, 5, 4), (2, 5, 3), (3, 5, 7), (4, 5, 9), (5, 5, 2), (6, 5, 5), (7, 5, 6), (8, 5, 1),
        (0, 6, 3), (1, 6, 5), (2, 6, 9), (3, 6, 4), (4, 6, 2), (5, 6, 8), (6, 6, 6), (7, 6, 1), (8, 6, 7),
        (0, 7, 4), (1, 7, 6), (2, 7, 8), (3, 7, 5), (4, 7, 7), (5, 7, 1), (6, 7, 3), (7, 7, 2), (8, 7, 9),
        (0, 8, 2), (1, 8, 1), (2, 8, 7), (3, 8, 9), (4, 8, 3), (5, 8, 6), (6, 8, 8), (7, 8, 4), (8, 8, 5)
    ]
    sudoku = Sudoku(3)
    sudoku._Sudoku__set_grid_from_var(lv)
    assert sudoku._Sudoku__grid == expected


@pytest.mark.parametrize("clause, expected", [
    ([1, 5, 9, 13], [[-1, -5], [-1, -9], [-1, -13], [-5, -9], [-5, -13], [-9, -13]]),
    ([1, 5], [[-1, -5]])
])
def test_clause_gen(clause, expected):
    assert Sudoku.clause_gen(clause) == expected


def test_sudoku_to_cnf():
    expected_cnf = [[-1, -21], [-1, -5], [-1, -17], [-1, -9], [-1, -33], [-1, -13], [-1, -49], [-1, -2], [-1, -3], [-1, -4],
                [-5, -17], [-5, -9], [-17, -33], [-5, -13], [-17, -49], [-5, -6], [-5, -7], [-5, -8], [-9, -13],
                [-33, -49], [-9, -10], [-9, -11], [-9, -12], [-13, -14], [-13, -15], [-13, -16], [1, 5, 9, 13],
                [1, 17, 33, 49], [1, 5, 17, 21], [-9, -29], [-17, -21], [-5, -21], [-17, -25], [-5, -37], [-17, -29],
                [-5, -53], [-17, -18], [-17, -19], [-17, -20], [-13, -25], [-21, -25], [-21, -37], [-21, -29],
                [-21, -53], [-21, -22], [-21, -23], [-21, -24], [-25, -29], [-37, -53], [-25, -26], [-25, -27],
                [-25, -28], [-29, -30], [-29, -31], [-29, -32], [17, 21, 25, 29], [5, 21, 37, 53], [9, 13, 25, 29],
                [-33, -53], [-33, -37], [-9, -25], [-33, -41], [-9, -41], [-33, -45], [-9, -57], [-33, -34], [-33, -35],
                [-33, -36], [-37, -49], [-37, -41], [-25, -41], [-37, -45], [-25, -57], [-37, -38], [-37, -39],
                [-37, -40], [-41, -45], [-41, -57], [-41, -42], [-41, -43], [-41, -44], [-45, -46], [-45, -47],
                [-45, -48], [33, 37, 41, 45], [9, 25, 41, 57], [33, 37, 49, 53], [-41, -61], [-49, -53], [-13, -29],
                [-49, -57], [-13, -45], [-49, -61], [-13, -61], [-49, -50], [-49, -51], [-49, -52], [-45, -57],
                [-53, -57], [-29, -45], [-53, -61], [-29, -61], [-53, -54], [-53, -55], [-53, -56], [-57, -61],
                [-45, -61], [-57, -58], [-57, -59], [-57, -60], [-61, -62], [-61, -63], [-61, -64], [49, 53, 57, 61],
                [13, 29, 45, 61], [41, 45, 57, 61], [-2, -22], [-2, -6], [-2, -18], [-2, -10], [-2, -34], [-2, -14],
                [-2, -50], [-2, -3], [-2, -4], [-6, -18], [-6, -10], [-18, -34], [-6, -14], [-18, -50], [-6, -7],
                [-6, -8], [-10, -14], [-34, -50], [-10, -11], [-10, -12], [-14, -15], [-14, -16], [2, 6, 10, 14],
                [2, 18, 34, 50], [2, 6, 18, 22], [-10, -30], [-18, -22], [-6, -22], [-18, -26], [-6, -38], [-18, -30],
                [-6, -54], [-18, -19], [-18, -20], [-14, -26], [-22, -26], [-22, -38], [-22, -30], [-22, -54],
                [-22, -23], [-22, -24], [-26, -30], [-38, -54], [-26, -27], [-26, -28], [-30, -31], [-30, -32],
                [18, 22, 26, 30], [6, 22, 38, 54], [10, 14, 26, 30], [-34, -54], [-34, -38], [-10, -26], [-34, -42],
                [-10, -42], [-34, -46], [-10, -58], [-34, -35], [-34, -36], [-38, -50], [-38, -42], [-26, -42],
                [-38, -46], [-26, -58], [-38, -39], [-38, -40], [-42, -46], [-42, -58], [-42, -43], [-42, -44],
                [-46, -47], [-46, -48], [34, 38, 42, 46], [10, 26, 42, 58], [34, 38, 50, 54], [-42, -62], [-50, -54],
                [-14, -30], [-50, -58], [-14, -46], [-50, -62], [-14, -62], [-50, -51], [-50, -52], [-46, -58],
                [-54, -58], [-30, -46], [-54, -62], [-30, -62], [-54, -55], [-54, -56], [-58, -62], [-46, -62],
                [-58, -59], [-58, -60], [-62, -63], [-62, -64], [50, 54, 58, 62], [14, 30, 46, 62], [42, 46, 58, 62],
                [-3, -23], [-3, -7], [-3, -19], [-3, -11], [-3, -35], [-3, -15], [-3, -51], [-3, -4], [-7, -19],
                [-7, -11], [-19, -35], [-7, -15], [-19, -51], [-7, -8], [-11, -15], [-35, -51], [-11, -12], [-15, -16],
                [3, 7, 11, 15], [3, 19, 35, 51], [3, 7, 19, 23], [-11, -31], [-19, -23], [-7, -23], [-19, -27],
                [-7, -39], [-19, -31], [-7, -55], [-19, -20], [-15, -27], [-23, -27], [-23, -39], [-23, -31],
                [-23, -55], [-23, -24], [-27, -31], [-39, -55], [-27, -28], [-31, -32], [19, 23, 27, 31],
                [7, 23, 39, 55], [11, 15, 27, 31], [-35, -55], [-35, -39], [-11, -27], [-35, -43], [-11, -43],
                [-35, -47], [-11, -59], [-35, -36], [-39, -51], [-39, -43], [-27, -43], [-39, -47], [-27, -59],
                [-39, -40], [-43, -47], [-43, -59], [-43, -44], [-47, -48], [35, 39, 43, 47], [11, 27, 43, 59],
                [35, 39, 51, 55], [-43, -63], [-51, -55], [-15, -31], [-51, -59], [-15, -47], [-51, -63], [-15, -63],
                [-51, -52], [-47, -59], [-55, -59], [-31, -47], [-55, -63], [-31, -63], [-55, -56], [-59, -63],
                [-47, -63], [-59, -60], [-63, -64], [51, 55, 59, 63], [15, 31, 47, 63], [43, 47, 59, 63], [-4, -24],
                [-4, -8], [-4, -20], [-4, -12], [-4, -36], [-4, -16], [-4, -52], [-8, -20], [-8, -12], [-20, -36],
                [-8, -16], [-20, -52], [-12, -16], [-36, -52], [4, 8, 12, 16], [4, 20, 36, 52], [4, 8, 20, 24],
                [-12, -32], [-20, -24], [-8, -24], [-20, -28], [-8, -40], [-20, -32], [-8, -56], [-16, -28], [-24, -28],
                [-24, -40], [-24, -32], [-24, -56], [-28, -32], [-40, -56], [20, 24, 28, 32], [8, 24, 40, 56],
                [12, 16, 28, 32], [-36, -56], [-36, -40], [-12, -28], [-36, -44], [-12, -44], [-36, -48], [-12, -60],
                [-40, -52], [-40, -44], [-28, -44], [-40, -48], [-28, -60], [-44, -48], [-44, -60], [36, 40, 44, 48],
                [12, 28, 44, 60], [36, 40, 52, 56], [-44, -64], [-52, -56], [-16, -32], [-52, -60], [-16, -48],
                [-52, -64], [-16, -64], [-48, -60], [-56, -60], [-32, -48], [-56, -64], [-32, -64], [-60, -64],
                [-48, -64], [52, 56, 60, 64], [16, 32, 48, 64], [44, 48, 60, 64]]
    sudoku = Sudoku(2)
    res = sudoku._Sudoku__sudoku_to_cnf()
    res_tuples = [tuple(sublist) for sublist in res]
    expected_cnf_tuples = [tuple(sublist) for sublist in expected_cnf]
    assert len(res) == len(expected_cnf)
    assert Counter(res_tuples) == Counter(expected_cnf_tuples)


def test_sudoku_solve():
    sudoku = Sudoku(2)
    sudoku.add((0, 0, 2))
    sudoku.add((2, 0, 3))
    sudoku.add((1, 1, 1))
    sudoku.add((3, 1, 2))
    sudoku.add((2, 2, 2))
    sudoku.add((3, 2, 4))
    sudoku.add((0, 3, 4))
    sudoku.add((1, 3, 2))
    res = sudoku.solve()
    assert res is True
    # Verify grid
    expected = [(0, 0, 2), (1, 0, 4), (2, 0, 3), (3, 0, 1),
                (0, 1, 3), (1, 1, 1), (2, 1, 4), (3, 1, 2),
                (0, 2, 1), (1, 2, 3), (2, 2, 2), (3, 2, 4),
                (0, 3, 4), (1, 3, 2), (2, 3, 1), (3, 3, 3)]
    for t in expected:
        assert sudoku.get_by_coordinates(t[0], t[1]) == t[2]
