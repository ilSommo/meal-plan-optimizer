# Meal plan optimizer

The aim of this project is to develop a meal plan optimizer using integer programming.

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