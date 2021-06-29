__version__ = '1.2.0'
__author__ = 'Martino Pulici'


import csv
import math

import pandas as pd
import pulp as pl

from meal_plan_optimizer.dishes import *


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
                # entered in minimization problems if all variables are integer
                # and the objective is improved
                if flag and sense == 1 and obj < ub:
                    # upper bound updated
                    ub = obj
                    # best problem updated
                    best = subprob.copy()
                # entered in maximization problems if all variables are integer
                # and the objective is improved
                if flag and sense == -1 and obj > lb:
                    # lower bound updated
                    lb = obj
                    # best problem updated
                    best = subprob.copy()
    return best


def meal_plan_optimizer_pulp():
    """
    Performs integer optimization using pulp.

    Returns
    -------
    int_probs : list
        Solved pulp problems.

    """
    # nutrient daily limits
    NUTRIENT_LIMITS = {'Energy': 2000,
                       'Fats': 70,
                       'Saturates': 20,
                       'Carbohydrates': 260,
                       'Sugars': 90,
                       'Proteins': 50
                       }

    TOLERANCE = 0.33

    # ingredient nutrients file
    df = pd.read_csv("data/food.csv")

    # dishes file
    with open("data/dish.csv") as file:
        reader = csv.reader(file)
        # dishes strings list
        dishes_list = list(reader)

    # unlimited dishes file
    with open("data/unlimited.txt") as file:
        reader = csv.reader(file)
        # unlimited dishes list
        unlimited_dishes = list(reader)[0]

    # list of food names
    labels = list(df['Food'])
    # dictionary of food costs
    costs = dict(zip(labels, df['Cost']))

    # dictionary of food nutrients
    nutrients = {}

    # cycle on foods
    for i in range(len(labels)):
        # dictionary of nutrients for specific food
        nutrients[labels[i]] = {}

        # cycle on nutrient limits
        for nutrient in NUTRIENT_LIMITS.keys():
            # nutrient quantities multiplied by 10 to convert to kg
            nutrients[labels[i]][nutrient] = df[nutrient][i] * 10

    # dish names list
    dishes_labels = []
    # dishes list
    dishes = []

    # cycle on dishes strings list
    for i in range(len(dishes_list)):
        # current dish
        d = dishes_list[i]
        # dish added to dishes list
        dishes.append(Dish(d[0], NUTRIENT_LIMITS))
        # dish name appended to list
        dishes_labels.append(d[0])

        # cycle on dish ingredients
        for j in range(1, len(d), 2):
            # current ingredient
            ingredient = d[j]
            # current quantity devided by 1000 to convert to kg
            quantity = float(d[j + 1]) / 1000
            # current ingredient cost added to dish cost
            dishes[i].cost += costs[ingredient] * quantity

            # cycle on ingredient nutrients
            for nut in dishes[i].nutrients.keys():
                # ingredient nutrient added to dish nutrient
                dishes[i].nutrients[nut] += nutrients[ingredient][nut] * quantity

    food_day_1 = pl.LpVariable.dicts(
        "Food_Day_1", dishes_labels, 0, cat='Integer')
    food_day_2 = pl.LpVariable.dicts(
        "Food_Day_2", dishes_labels, 0, cat='Integer')
    food_day_3 = pl.LpVariable.dicts(
        "Food_Day_3", dishes_labels, 0, cat='Integer')
    food_day_4 = pl.LpVariable.dicts(
        "Food_Day_4", dishes_labels, 0, cat='Integer')
    food_day_5 = pl.LpVariable.dicts(
        "Food_Day_5", dishes_labels, 0, cat='Integer')

    # LpVariable list
    foods = [food_day_1, food_day_2, food_day_3, food_day_4, food_day_5]

    prob_day_1 = pl.LpProblem("Day_1", pl.LpMinimize)
    prob_day_2 = pl.LpProblem("Day_2", pl.LpMinimize)
    prob_day_3 = pl.LpProblem("Day_3", pl.LpMinimize)
    prob_day_4 = pl.LpProblem("Day_4", pl.LpMinimize)
    prob_day_5 = pl.LpProblem("Day_5", pl.LpMinimize)

    # LpProblems list
    probs = [prob_day_1, prob_day_2, prob_day_3, prob_day_4, prob_day_5]

    # cycle on problems
    for i in range(len(probs)):
        # objective added to problem
        probs[i] += pl.lpSum([dish.cost * foods[i][dish.name]
                             for dish in dishes])

        # cycle on nutrients
        for nut in NUTRIENT_LIMITS.keys():
            # minimum nutrient quantity constraint added to problem
            probs[i] += pl.lpSum([dish.nutrients[nut] * foods[i][dish.name]
                                 for dish in dishes]) >= NUTRIENT_LIMITS[nut] * (1 - TOLERANCE)
            # maximum nutrient quantity constraint added to problem
            probs[i] += pl.lpSum([dish.nutrients[nut] * foods[i][dish.name]
                                 for dish in dishes]) <= NUTRIENT_LIMITS[nut] * (1 + TOLERANCE)
        # cycle on dishes
        for j in range(len(probs[i].variables())):
            # maximum number of servings for dish added
            probs[i] += probs[i].variables()[j] <= 3

    # integer problems list
    int_probs = []

    # cycle on problems
    for i in range(0, len(probs)):

        # cycle on previous problems
        for j in range(0, i):

            # cycle on previous problem dishes
            for k in range(len(int_probs[j].variables())):

                # entered if dish has already been chosen for a previous problem
                # and it is not an unlimited dish
                if int_probs[j].variables()[k].varValue and not unlimited_dish(
                        str(int_probs[j].variables()[k]), unlimited_dishes):

                    # dish quantity set to 0
                    probs[i] += probs[i].variables()[k] == 0

                # entered if dish is already chosen for one of the last two
                # problems and it is an unlimited dish
                if ((j == i - 1) or (j == i - 2)) and int_probs[j].variables()[
                        k].varValue and unlimited_dish(str(int_probs[j].variables()[k]), unlimited_dishes):

                    # dish quantity set to 0
                    probs[i] += probs[i].variables()[k] == 0

        # integer problem added to list
        int_probs.append(probs[i])
        # last problem solved
        int_probs[-1].solve()

    return int_probs
