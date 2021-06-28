__version__ = '1.0.1'
__author__ = 'Martino Pulici'


import csv

import pandas as pd
import pulp

from meal_plan_optimizer.dishes import *
from meal_plan_optimizer.branch_and_bound import *

# nutrient daily limits
NUTRIENT_LIMITS = {'Energy': 2000,
                   'Fat': 70,
                   'Saturates': 20,
                   'Carbohydrates': 260,
                   'Sugars': 90,
                   'Protein': 50
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

food_day_1 = pulp.LpVariable.dicts("Food_Day_1", dishes_labels, 0)
food_day_2 = pulp.LpVariable.dicts("Food_Day_2", dishes_labels, 0)
food_day_3 = pulp.LpVariable.dicts("Food_Day_3", dishes_labels, 0)
food_day_4 = pulp.LpVariable.dicts("Food_Day_4", dishes_labels, 0)
food_day_5 = pulp.LpVariable.dicts("Food_Day_5", dishes_labels, 0)

# LpVariable list
foods = [food_day_1, food_day_2, food_day_3, food_day_4, food_day_5]

prob_day_1 = pulp.LpProblem("Day_1", pulp.LpMinimize)
prob_day_2 = pulp.LpProblem("Day_2", pulp.LpMinimize)
prob_day_3 = pulp.LpProblem("Day_3", pulp.LpMinimize)
prob_day_4 = pulp.LpProblem("Day_4", pulp.LpMinimize)
prob_day_5 = pulp.LpProblem("Day_5", pulp.LpMinimize)

# LpProblems list
probs = [prob_day_1, prob_day_2, prob_day_3, prob_day_4, prob_day_5]

# cycle on problems
for i in range(len(probs)):
    # objective added to problem
    probs[i] += pulp.lpSum([dish.cost * foods[i][dish.name]
                           for dish in dishes])

    # cycle on nutrients
    for nut in NUTRIENT_LIMITS.keys():
        # minimum nutrient quantity constraint added to problem
        probs[i] += pulp.lpSum([dish.nutrients[nut] * foods[i][dish.name]
                               for dish in dishes]) >= NUTRIENT_LIMITS[nut] * (1 - TOLERANCE)
        # maximum nutrient quantity constraint added to problem
        probs[i] += pulp.lpSum([dish.nutrients[nut] * foods[i][dish.name]
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
    int_probs.append(branch_and_bound(probs[i]))
    # last problem solved
    int_probs[-1].solve(pl.PULP_CBC_CMD(msg=0))

print("TOTAL COST = " +
      "{0:.2f}".format(pulp.value(sum([n.objective for n in int_probs]))) +
      " €")

for day in ["_Day_1_", "_Day_2_", "_Day_3_", "_Day_4_", "_Day_5_"]:
    print()
    print(day[1:6].upper())

    for prob in int_probs:
        for v in prob.variables():
            if v.varValue and day in v.name:
                print(v.name[11:] + " = {0:.0f}".format(v.varValue))
