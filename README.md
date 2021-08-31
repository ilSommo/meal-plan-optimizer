# Meal plan optimizer

The aim of this project is to develop a meal plan optimizer using integer programming.

The program outputs a meal plan for a 5-day week with 3  characteristics:

* Respect of Reference Daily Intakes
  * Calories: 2000 kcal
  * Fats: 70 g
  * Saturates: 20 g
  * Carbohydrates: 260 g
  * Sugars: 90 g
  * Proteins: 50 g
* Variation in dishes
  * Limit of 3 daily servings per dish
  * Limit of 1 day every 3 days for fruit and vegetables
  * Limit of 1 day a week per dish
* Minization of daily expense

In order to satisfy the constraints, a mix of PuLP functions and an original implementation of the branch-and-bound algorithm is exploited.

## Setup

### To run

```console
$ make setup
```

### To develop

```console
$ make dev
```

## Run

```console
$ python meal-plan-optimizer.py
```

## Remove

```console
$ make rm
```

## Documentation

To browse documentation, open `docs/index.html` with a web browser.