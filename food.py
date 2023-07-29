from water_library import *


class Food:
    def __init__(self, period, average=0, household_members=1):
        self.unit = ""
        self.period = period
        self.food_dict = {}  # Dictionary of Food with values being dicts themselves of characteristics
        self.average = average  # the value of average is stored here
        self.house_members = household_members
        self.user_foods = []  # All foods that the users added should be stored here
        self.user_wfs = []  # The water footprints of the users should be stored here. Sum is to be calculated from

    def use_food_csv(self, file, food, unit, serving=None, category=None, explanation=None, other=None):
        """Returns a list of dictionaries of food items and values being their characteristics as individual
        dictionaries"""

        self.unit = unit
        the_list = []
        foods_only = []

        def import_function():
            """Returns food_dict with food name as keys and dictionaries of its characteristics as values."""
            in_list = create_value_dict(["Formatted", serving, self.unit, category, explanation, other],
                                        the_list, True, "Formatted")
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

    def print_foods(self):
        i = 1
        for food in self.food_dict:
            print(f"{i}. {food}")
            i += 1

    def check_food_item(self, user_input):
        """Returns food and wf as a dict with same keys among updating the object attributes and other things"""

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
        if food in self.user_foods:
            print(f"{food} already added.")
            return

        # Adding the food to users lists of foods and water footprints
        try:
            wf = float(self.food_dict[food][self.unit])
            serving = self.food_dict[food]['Serving Size']
            return {'food': food, 'wf': wf, 'Serving Size': serving}
        except KeyError:
            print(f"{user_input} is out of range or not in our database. Maybe you misspelled?")

    def add_food_item(self, food, wf, times):
        """Adds the water footprint of the food item in a list of food water footprints"""
        self.user_wfs.append(wf * times)
        self.user_foods.append(food)
        print(f"{food} added")

    def calculate_food_wf(self):
        """Calculates the total water footprint of the people in the household"""
        return f"Your water footprint is {sum(self.user_wfs) * self.house_members} in {self.unit} per {self.period}."

    # TODO: Create an asking for explanations for the water footprint of each item that the user consumes.
    # TODO: Add a meal_ingredients function
