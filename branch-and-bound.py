import pulp as pl
import copy
import math

def branch_and_bound(prob):
    lb = float('-inf')
    ub = float('inf')
    unexpanded = [(prob, lb, ub)]
    while unexpanded:
        subprob = unexpanded.pop(-1)[0]
        subsol = subprob.solve()
        if subsol == 1:
            obj = pl.value(subprob.objective)
            flag = True
            var = subprob.variables()
            for v in var:
                if not v.varValue.is_integer():
                    flag = False
                    ub_prob=subprob.copy()
                    ub_prob += v <= math.floor(v.varValue)
                    unexpanded.append((ub_prob, lb, obj))
                    lb_prob=subprob.copy()
                    lb_prob += v >= math.ceil(v.varValue)
                    unexpanded.append((lb_prob, obj, ub))
                    break
            if flag and prob.sense==1:
                if obj < ub:
                    ub = obj
                    best=subprob.copy()
                    for node in unexpanded:
                        if node[1] > ub:
                            unexpanded.remove(node)
            if flag and prob.sense==-1:
                if obj > lb:
                    lb = obj
                    best=subprob.copy()
                    for node in unexpanded:
                        if node[2] < lb:
                            unexpanded.remove(node)
    return best