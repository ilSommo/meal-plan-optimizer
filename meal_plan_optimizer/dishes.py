__version__ = '1.1.0'
__author__ = 'Martino Pulici'


class Dish:
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
