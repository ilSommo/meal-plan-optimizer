"""
@package meal_plan_optimizer

Meal plan optimizer project package.
"""


__version__ = '1.0.0-rc.2'
__author__ = 'Martino Pulici'


import math

import pulp as pl


class dish:
    """
    Class containing dish attributes.

    Attributes
    ----------
    name : str
        Name of the dish.
    cost : float
        Cost of the dish.
    nutrients : dict
        Nutrients of the dish

    Methods
    -------
    __init__(self, name, nutrient_limits)
        Initializes a dish.

    """
    name = ""
    cost = 0
    nutrients = {}

    def __init__(self, name, nutrient_limits):
        """
        Initializes a dish.

        Parameters
        ----------
        self : dish
            Dish to initialize.
        name : str
            Dish name.
        nutrient_limits : dict
            Nutrient limits dictionary.

        """
        self.name = name
        self.nutrients = {nut: 0 for nut in nutrient_limits.keys()}


def branch_and_bound(prob):
    """
    Performs the branch and bound algorithm on a pulp problem.

    Parameters
    ----------
    prob : pulp.pulp.LpProblem
        Real value optimization problem to solve using integer programming.

    Returns
    -------
    best : pulp.pulp.LpProblem
        Integer value.

    """
    sense = prob.sense
    # 1 if LpMinimize, -1 if LpMaximize
    tup_idx = 1 if sense == 1 else 2
    # used for list sorting
    reverse_bool = True if sense == 1 else False
    # used for list sorting
    lb = float('-inf')
    # lower boundary
    ub = float('inf')
    # upper boundary
    unexpanded = [(prob, lb, ub)]
    # list of unexpanded subproblems
    while unexpanded:
        # entered while the list of subproblems is not empty
        unexpanded.sort(key=lambda tup: tup[tup_idx], reverse=reverse_bool)
        # list sorting to optimize computation time
        node = unexpanded.pop(-1)
        # subproblem choice
        if (sense == 1 and node[1] <= ub) or (sense == -1 and node[2] >= lb):
            # entered if boundaries are compatible with found solutions
            subprob = node[0]
            # subproblem to solve
            subsol = subprob.solve()
            # subproblem solving attempt
            if subsol == 1:
                # entered if solution found
                obj = pl.value(subprob.objective)
                # subproblem objective
                flag = True
                # used for boundaries update
                var = subprob.variables()
                # list of subproblem variables
                for v in var:
                    # cycle on list of subproblem variables
                    if not v.varValue.is_integer():
                        # entered if variable v is not integer
                        flag = False
                        # used for boundaries update
                        ub_prob = subprob.copy()
                        # new subproblem
                        ub_prob += v <= math.floor(v.varValue)
                        # upper boundary added
                        unexpanded.append((ub_prob, lb, obj))
                        # subproblem appended to list
                        lb_prob = subprob.copy()
                        # new subproblem
                        lb_prob += v >= math.ceil(v.varValue)
                        # lower boundary added
                        unexpanded.append((lb_prob, obj, ub))
                        # subproblem appended to list
                        break
                        # for cycle broken after first non-integer variable
                if flag and sense == 1 and obj < ub:
                    # entered in minimization problems if all variables are
                    # integer and the objective is improved
                    print("\n" + str(obj))
                    for v in var:
                        if v.varValue != 0:
                            print(str(v) + " = {0:.0f}".format(v.varValue))
                    ub = obj
                    # upper bound updated
                    best = subprob.copy()
                    # best problem updated
                if flag and sense == -1 and obj > lb:
                    # entered in maximization problems if all variables are
                    # integer and the objective is improved
                    print("\n" + str(obj))
                    for v in var:
                        if v.varValue != 0:
                            print(str(v) + " = {0:.0f}".format(v.varValue))
                    lb = obj
                    # lower bound updated
                    best = subprob.copy()
                    # best problem updated
    return best


def unlimited_dish(string, unlimited_dishes):
    """
    Checks if a dish is part of the unlimited dishes list.

    Parameters
    ----------
    string : str
        Dish to check.
    unlimited_dishes : list
        List of unlimited dishes.

    Returns
    -------
    bool
        True if dish is part of the unlimited dishes list, False otherwise.

    """
    for dish in unlimited_dishes:
        if dish in string:
            return True
    return False