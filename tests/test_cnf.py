import sys
import os
import pytest
from typing import Optional

# Moves up a level from the test file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cnf import CNF


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
    cnf = CNF([[1, 2], [2, -3, 4], [-1, -2], [-1, -2, -3], [1]], [None, None, None, None])
    result = cnf.evaluate(list_var)
    assert result is expected
