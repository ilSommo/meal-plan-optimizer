__version__ = '1.0.0-alpha'
__author__ = 'Martino Pulici'


import math

import pulp as pl


def branch_and_bound(prob):
    sense = prob.sense
    tup_idx = 1 if sense == 1 else 2
    reverse_bool = True if sense == 1 else False
    lb = float('-inf')
    ub = float('inf')
    unexpanded = [(prob, lb, ub)]
    while unexpanded:
        unexpanded.sort(key=lambda tup: tup[tup_idx], reverse=reverse_bool)
        node = unexpanded.pop(-1)
        if (sense == 1 and node[1] <= ub) or (sense == -1 and node[2] >= lb):
            subprob = node[0]
            subsol = subprob.solve()
            if subsol == 1:
                obj = pl.value(subprob.objective)
                flag = True
                var = subprob.variables()
                for v in var:
                    if not v.varValue.is_integer():
                        flag = False
                        ub_prob = subprob.copy()
                        ub_prob += v <= math.floor(v.varValue)
                        unexpanded.append((ub_prob, lb, obj))
                        lb_prob = subprob.copy()
                        lb_prob += v >= math.ceil(v.varValue)
                        unexpanded.append((lb_prob, obj, ub))
                        break
                if flag and sense == 1 and obj < ub:
                    print("\n" + str(obj))
                    for v in var:
                        if v.varValue != 0:
                            print(v, v.varValue)
                    ub = obj
                    best = subprob.copy()
                if flag and sense == -1 and obj > lb:
                    print("\n" + str(obj))
                    for v in var:
                        if v.varValue != 0:
                            print(v, v.varValue)
                    lb = obj
                    best = subprob.copy()
    return best
