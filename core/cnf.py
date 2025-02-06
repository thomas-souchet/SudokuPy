from copy import deepcopy
from typing import Optional, Tuple


class CNF:
    """! The conjunctive normal form class.
    Defines the data structure used to represent a boolean logic formula in the conjunctive normal form.
    """

    def __init__(self, formula: list[list[int]], list_var: list[Optional[bool]]):
        """! The CNF class initializer.
        @param formula  An 2-dimensional array containing all the clauses that are in the conjunctive normal form.
        @param list_var  An 1-dimensional array containing all the value of the variables that are in the CNF.
        @return  An instance of the CNF class initialized with the specified formula.
        """
        self.__initial_formula = deepcopy(formula)
        self.__actual_formula = deepcopy(formula)
        self.__initial_var = list_var[:]
        self.__list_var = list_var[:]
        self.__history = []
        self.__satisfiable = None
        # Simplify the initial formula with the known variables
        for cons_index in range(len(self.__list_var)):
            # Remove literal if he is constrained by a variable
            if self.__list_var[cons_index] is True:
                self.remove_literal(cons_index + 1)
            elif self.__list_var[cons_index] is False:
                self.remove_literal(-(cons_index + 1))
        # Reset the history of the changes made by remove_literal because it's the initial state
        self.__initial_formula = deepcopy(self.__actual_formula)
        self.__list_var = list_var[:]
        self.__history = []

    def get_initial_cnf(self) -> list[list[int]]:
        """! Get the Initial CNF formula.
        @return  A CNF formula.
        """
        return self.__initial_formula

    def get_actual_cnf(self) -> list[list[int]]:
        """! Get the Actual CNF formula.
        @return  A CNF formula.
        """
        return self.__actual_formula

    def get_list_var(self) -> list[Optional[bool]]:
        """! Get the list of the values for each variable in the CNF.
        @return  The actual list of values formula.
        """
        return self.__list_var

    def get_satisfiable(self) -> Optional[bool]:
        """! Get if the actual CNF formula is satisfiable.
        @return  True if the CNF formula is satisfiable.
        """
        return self.__satisfiable

    def get_history(self) -> list[Tuple[int, bool]]:
        """! Get the history of the CNF formula.
        @return  List of all the changes made in the formula.
        """
        return self.__history

    @staticmethod
    def evaluate_var(variable: int, valuation: Optional[bool]) -> Optional[bool]:
        """! Evaluate a logic variable in a CNF clause.
        @param variable  The variable to be evaluated.
        @param valuation  The valuation of the variable.
        @return  The value of the evaluated variable.
        """
        if (valuation and variable > 0) or (valuation is False and variable < 0):
            return True
        elif (valuation is False and variable > 0) or (valuation is True and variable < 0):
            return False
        return None

    @staticmethod
    def evaluate_clause(clause: list[int], list_var: list[Optional[bool]]) -> Optional[bool]:
        """! Evaluate a clause in a CNF.
        @param clause  The clause to be evaluated.
        @param list_var  The valuation list for each of the variables.
        @return  The value of the evaluated clause.
        """
        if not clause:
            return False

        false_count = 0
        for cl in clause:
            # Evaluate each var
            valuation = CNF.evaluate_var(cl, list_var[abs(cl) - 1])
            if valuation:
                # One variable True then the clause is True
                return True
            if valuation is False:
                false_count += 1
        # If all literals are False then the clause is False
        if false_count == len(clause):
            return False
        return None

    def evaluate(self):
        """! Evaluate the CNF.
        """
        if not self.__actual_formula:
            self.__satisfiable = True
            return
        true_count = 0
        for cl in self.__actual_formula:
            val = CNF.evaluate_clause(cl, self.__list_var)
            if val is False:
                # The formula is wrong, because it is a conjunction
                self.__satisfiable = False
                return
            if val:
                true_count += 1
        if true_count == len(self.__actual_formula):
            self.__satisfiable = True
            return
        self.__satisfiable = None

    def remove_literal(self, literal: int):
        """! Simply the CNF by putting a variable to true or false to remove a literal.
        @param literal  The literal to be removed.
        """
        if literal >= 0:
            self.__history.append((abs(literal) - 1, True))
            self.__list_var[abs(literal) - 1] = True
        else:
            self.__history.append((abs(literal) - 1, False))
            self.__list_var[abs(literal) - 1] = False
        i = 0
        while i < len(self.__actual_formula):
            j = 0
            while j < len(self.__actual_formula[i]):
                if self.__actual_formula[i][j] == literal:
                    self.__actual_formula.remove(self.__actual_formula[i])
                    i -= 1
                    break
                elif -self.__actual_formula[i][j] == literal:
                    self.__actual_formula[i].remove(self.__actual_formula[i][j])
                else:
                    j += 1
            i += 1
        self.evaluate()

    def restore_state(self, history: list[Tuple[int, bool]]):
        """! Restore the CNF to a given state using the given history.
        @param history  The history of changes made to the CNF.
        """
        self.__actual_formula = deepcopy(self.__initial_formula)
        self.__list_var = self.__initial_var[:]
        self.__history = []
        for change in history:
            lit = change[0] + 1
            for clause in self.__actual_formula:
                if lit in clause or -lit in clause:
                    if change[1] is True:
                        self.remove_literal(lit)
                        break
                    elif change[1] is False:
                        self.remove_literal(-lit)
                        break
