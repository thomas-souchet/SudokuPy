from typing import Optional


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
        self.__formula = formula
        self.__list_var = list_var

    def get_cnf(self):
        """! Get the CNF formula.
        @return  The actual CNF formula.
        """
        return self.__formula

    def get_list_var(self):
        """! Get the list of the values for each variable in the CNF.
        @return  The actual list of values formula.
        """
        return self.__formula

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

    def evaluate(self, list_var: list[Optional[bool]]) -> Optional[bool]:
        """! Evaluate a clause in a CNF.
        @param list_var  The valuation list for each of the variables.
        @return  The value of the evaluated CNF.
        """
        if not self.__formula:
            return True
        true_count = 0
        for cl in self.__formula:
            val = CNF.evaluate_clause(cl, list_var)
            if val is False:
                # The formula is wrong, because it is a conjunction
                return False
            if val:
                true_count += 1
        if true_count == len(self.__formula):
            return True
        return None
