from water_library import *


class Food:
    def __init__(self, period, average=0, household_members=1):
        """
        Initialize the Food class.

        Parameters:
            period (str): The time period for which the water footprint is calculated (e.g., 'week', 'day').
            average (int or float, optional): The average value used in calculations.
            household_members (int, optional): The number of members in the household.
        """
        # Keys of dictionaries in self.food_dict
        self.unit = ""
        self.serving = None
        self.category = None
        self.explanation = None
        self.other = None

        self.period = period
        self.food_dict = {}  # Dictionary of Food with values being dicts themselves of characteristics
        self.average = average  # The value of average is stored here
        self.household_members = household_members
        self.user_foods = {}  # All foods that the users added should be stored here with the values being their water footprints
        self.user_wfs = []  # The water footprints of the users should be stored here. Sum is to be calculated from

    def load_food_csv(self, file, food, unit, serving=None, category=None, explanation=None, other=None):
        """
        Returns a list of dictionaries of food items and values being their characteristics as individual dictionaries.

        Parameters:
            file (str): The CSV file containing the food data.
            food (str): The title of the column containing food names.
            unit (str): The unit of water footprint (e.g., 'Litres' or 'Gallons').
            serving (str, optional): The title of the column containing serving size data.
            category (str, optional): The title of the column containing food categories.
            explanation (str, optional): The title of the column containing explanations for food items.
            other (str, optional): The title of additional column containing other information.
        """
        self.unit = unit
        self.serving = serving
        self.category = category
        self.explanation = explanation
        self.other = other

        the_list = []
        foods_only = []

        def import_function():
            """Returns food_dict with food name as keys and dictionaries of its characteristics as values."""
            in_list = create_value_dict(prospective_keys=["Formatted", serving, self.unit, category, explanation, other],
                                        dict_list=the_list, replace_spaces=True, formatted_title="Formatted")
            i = 0
            for _ in the_list:
                value_dict = in_list[i]
                self.food_dict[the_list[i][food]] = value_dict
                i += 1
            return self.food_dict

        dict_obj = import_csv(file)
        for row in dict_obj:
            the_list.append(row)
            foods_only.append(row[food])
        return import_function()

    def display_available_foods(self):
        """
        Print the list of available food items.
        """
        i = 1
        for food in self.food_dict:
            print(f"{i}. {food}")
            i += 1

    def check_food_item(self, user_input):
        """
        Check if the user input corresponds to a valid food item.

        Parameters:
            user_input (str or int): The user input for food item (name or serial number).

        Returns:
            dict or None: A dictionary containing food and water footprint details if the food item is valid.
        """
        food = user_input
        food = format_data(food, True)  # Formatting argument to number or changing it to lowercase and removing spaces

        # If user input serial number of the food item from the list
        if isinstance(food, int):
            i = 1
            for f in self.food_dict:
                if i == food:
                    food = f
                    break
                i += 1
        # Finding user input from food_dict and turning user input to actual key in food_dict.
        for f in self.food_dict:
            if self.food_dict[f]["Formatted"] == food:
                food = f

        # Checking if user has already added the food item.
        if food in self.user_foods.keys():
            print(f"{food} already added.")
            return

        # Adding the food to users lists of foods and water footprints
        try:
            wf = float(self.food_dict[food][self.unit])
            serving = self.food_dict[food][self.serving]
            return {'food': food, 'wf': wf, 'Serving Size': serving}
        except KeyError:
            print(f"{user_input} is out of range or not in our database. Maybe you misspelled?")

    def add_food_item(self, food, wf, times):
        """
        Add the water footprint of the food item to the list of food water footprints.

        Parameters:
            food (str): The name of the food item.
            wf (float): The water footprint of the food item.
            times (float): The number of times the food item is consumed.
        """
        self.user_foods[food] = wf
        self.user_wfs.append(wf * times)
        print(f"{food} added")

    def calculate_food_wf(self):
        """
        Calculate the total water footprint of the people in the household.

        Returns:
            str: A string representing the calculated water footprint.
        """
        return f"Your water footprint is {sum(self.user_wfs) * self.household_members} in {self.unit} per {self.period}."
