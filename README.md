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

### Setup using makefile

1. Install `pyenv` (https://github.com/pyenv/pyenv)
2. Run:
   ```console
   $ make
   ```

### Manual setup

The creation of a virtual enviornment using `pyenv` is reccomended: to only install the required packages with `pip` skip to step 3.

1. Install `pyenv` (https://github.com/pyenv/pyenv)
2. Create a virtual environment using `pyenv` and activate it:
   ```console
    $ pyenv install 3.8.5
    $ pyenv virtualenv 3.8.5 meal-plan-optimizer
    $ pyenv local meal-plan-optimizer
    ```
3. Install package requirements:
    ```console
    $ pip install -r requirements.txt
    ```

### Deleting the virtual enviornment

```console
$ pyenv virtualenv-delete meal-plan-optimizer
```

## Documentation

To browse documentation, open `docs/index.html` with a web browser.

## Package requirements

`python 3.8.5`

`jupyter 1.0.0`  
`pandas 1.1.5`  
`pulp 2.4`