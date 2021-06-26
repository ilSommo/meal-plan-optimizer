__version__ = '1.0.0-rc.2'
__author__ = 'Martino Pulici'


import math

import pulp as pl


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
    # 1 if LpMinimize, -1 if LpMaximize
    sense = prob.sense
    # used for list sorting
    tup_idx = 1 if sense == 1 else 2
    # used for list sorting
    reverse_bool = True if sense == 1 else False
    # lower boundary
    lb = float('-inf')
    # upper boundary
    ub = float('inf')
    # list of unexpanded subproblems
    unexpanded = [(prob, lb, ub)]
    # entered while the list of subproblems is not empty
    while unexpanded:
        # list sorting to optimize computation time
        unexpanded.sort(key=lambda tup: tup[tup_idx], reverse=reverse_bool)
        # subproblem choice
        node = unexpanded.pop(-1)
        # entered if boundaries are compatible with found solutions
        if (sense == 1 and node[1] <= ub) or (sense == -1 and node[2] >= lb):
            # subproblem to solve
            subprob = node[0]
            # subproblem solving attempt
            subsol = subprob.solve()
            # entered if solution found
            if subsol == 1:
                # subproblem objective
                obj = pl.value(subprob.objective)
                # used for boundaries update
                flag = True
                # list of subproblem variables
                var = subprob.variables()
                # cycle on list of subproblem variables
                for v in var:
                    # entered if variable v is not integer
                    if not v.varValue.is_integer():
                        # used for boundaries update
                        flag = False
                        # new subproblem
                        ub_prob = subprob.copy()
                        # upper boundary added
                        ub_prob += v <= math.floor(v.varValue)
                        # subproblem appended to list
                        unexpanded.append((ub_prob, lb, obj))
                        # new subproblem
                        lb_prob = subprob.copy()
                        # lower boundary added
                        lb_prob += v >= math.ceil(v.varValue)
                        # subproblem appended to list
                        unexpanded.append((lb_prob, obj, ub))
                        # for cycle broken after first non-integer variable
                        break
                # entered in minimization problems if all variables are integer and the objective is improved
                if flag and sense == 1 and obj < ub:
                    print("\n" + str(obj))
                    for v in var:
                        if v.varValue != 0:
                            print(str(v) + " = {0:.0f}".format(v.varValue))
                    # upper bound updated
                    ub = obj
                    # best problem updated
                    best = subprob.copy()
                # entered in maximization problems if all variables are 
                if flag and sense == -1 and obj > lb:
                    print("\n" + str(obj))
                    for v in var:
                        if v.varValue != 0:
                            print(str(v) + " = {0:.0f}".format(v.varValue))
                    # lower bound updated
                    lb = obj
                    # best problem updated
                    best = subprob.copy()
    return best