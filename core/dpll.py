from copy import deepcopy

from core.cnf import CNF


class DPLL:
    """! The DPLL (Davis–Putnam–Logemann–Loveland) class.
    Defines the data structure and the algorithm to solve a logic formula.
    """

    def __init__(self, base_formula: CNF):
        """! The DPLL class initializer.
        @param base_formula The formula to solve.
        @return  An instance of the DPLL class initialized with the specified formula.
        """
        self.__formula: CNF = base_formula
        self.__list_simplifications: list[int] = []

    def __solve(self) -> bool:
        """! Find recursively if a CNF formula is satisfiable or not using DPLL algorithm.
        @return  Boolean indicating if the CNF formula is satisfiable or not.
        """
        if self.__formula.get_satisfiable() is True:
            return True
        # Handle edge cases and initialisation of tree progression
        if not self.__formula.get_history():
            if not self.__formula.get_actual_cnf():
                return True
            if [] in self.__formula.get_actual_cnf():
                return False
            # First progression
            self.__progress()
            return self.__solve()
        # Progress in the tree path
        old_history = self.__formula.get_history()
        self.__progress()
        # If no changes made go back
        if old_history == self.__formula.get_history():
            self.__back()
        # If we can't go back then the formula is unsatisfiable
        if not self.__formula.get_history():
            return False
        # Recursive to try solving the formula with the changes made
        return self.__solve()

    def __progress(self):
        """! Progress in the tree to make either a simplification following DPLL rules or assign a variable to True."""
        # Exit if elements are empty
        if not self.__formula.get_list_var() or not self.__formula.get_actual_cnf():
            return

        # Find DPLL simplification
        dpll_litt = -1
        dpll_simpl = False
        literals = []

        # Var which will be set if there is no DPLL simplifications
        editable_vars = []
        for v_index in range(len(self.__formula.get_list_var())):
            if self.__formula.get_list_var()[v_index] is None:
                editable_vars.append({"v_index": v_index, "occurrences": 0})

        for cl in self.__formula.get_actual_cnf():
            # Find unitary clause
            if len(cl) == 1:
                dpll_litt = cl[0]
                dpll_simpl = True
                break
            # Find out if there is a pure literal
            for litt in cl:
                add = True
                for el in literals:
                    if litt == el[0]:
                        add = False
                        break
                    elif litt == -el[0]:
                        add = False
                        el[1] = False
                        break
                if add:
                    literals.append([litt, True])
            for ev_index in range(len(editable_vars)):
                editable_vars[ev_index]["occurrences"] += cl.count(editable_vars[ev_index]["v_index"]+1)
                editable_vars[ev_index]["occurrences"] += cl.count(-editable_vars[ev_index]["v_index"]+1)
        # Check whether a pure literal has been found if there is no unitary clause
        if dpll_simpl is False:
            for el in literals:
                if el[1]:
                    dpll_litt = el[0]
                    dpll_simpl = True
                    break
        # DPLL Simplification
        if dpll_simpl:
            self.__formula.remove_literal(dpll_litt)
            self.__list_simplifications.append(abs(dpll_litt)-1)
            return
        # If there is no simplification progress in the tree
        if len(editable_vars) > 0:
            choice = max(editable_vars, key=lambda x: x['occurrences'])
            self.__formula.remove_literal(choice['v_index']+1)

    def __back(self):
        """! Go back in the tree to change the assignation of a variable to False. (Backtracking)"""
        # Exit if elements are empty
        if not self.__formula.get_list_var() or not self.__formula.get_actual_cnf() or not self.__formula.get_history():
            return
        # Last change index
        change_list = deepcopy(self.__formula.get_history())
        change_index = len(change_list) - 1
        # Go back in history to find the variable to modify
        while (change_index >= 0
               and (change_list[change_index][1] is False or change_list[change_index][0] in self.__list_simplifications)):
            change_index -= 1
        # If all possible returns have already been made (all changes to False) then return the formula to
        # its initial state and empty the list of changes and returns
        if change_index < 0:
            self.__formula.restore_state([])
            self.__formula.evaluate()
            self.__list_simplifications = []
            return
        # Cancel old changes
        cancel_index = len(change_list) - 1
        # Erase part of the history
        while cancel_index > change_index:
            if change_list[cancel_index][0] in self.__list_simplifications:
                self.__list_simplifications.remove(change_list[cancel_index][0])
            change_list.remove(change_list[cancel_index])
            cancel_index -= 1
        # Make the modification
        change_list[change_index] = (change_list[change_index][0], False)
        self.__formula.restore_state(change_list)


