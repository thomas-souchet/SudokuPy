import sys
import os
import pytest
from copy import deepcopy
from typing import Optional, Tuple

# Moves up a level from the test file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cnf import CNF
from core.dpll import DPLL

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
