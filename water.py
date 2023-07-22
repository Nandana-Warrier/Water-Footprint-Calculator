import csv
import re


def format_data(data, replace_spaces):
    if replace_spaces:
        data = data.replace(" ", "")
    if data.isdigit():
        return int(data)
    else:
        if "/" in data or "," in data:
            return re.split("/,", data)
        return str(data).lower()


class Water:
    def __init__(self, average, household_members=1):
        self.unit = ""
        self.food_dict = {}  # Dictionary of Food with values being dicts themselves of characteristics
        self.average = average  # the value of average is stored here
        self.household_members = household_members
        self.user_foods = []  # All foods that the users added should be stored here
        self.user_wfs = []  # The water footprints of the users should be stored here. Sum is to be calculated from
        # this list

    def import_from_csv(self, file, food, unit, serving=None, category=None, explanation=None, other=None):
        """Returns a dictionary of food items and their water footprints.
        IMPORTANT: The files should have titles 'Food' and 'Gallons' or 'Litres'. Pass the unit as argument."""

        self.unit = unit
        the_list = []

        def create_value_dict():
            """Returns list of dictionaries with characteristics like Litres, Gallons, Serving that will be values
            for each food name in food_dict"""
            value_list = []  # Values of Foods which are dicts of characteristics like Gallons, Litres, Serving Size
            for dic in the_list:
                a_dict = {"Formatted": format_data(dic[food], True), self.unit: int(dic[self.unit])}
                a_dict.update({"Serving": int(dic[serving])} if serving is not None else {})
                a_dict.update({"Category": dic[category].split(", ")} if category is not None else {})
                a_dict.update({"Explanation": dic[explanation]} if explanation is not None else {})
                a_dict.update({"Other": format_data(dic[other], True)} if other is not None else {})
                value_list.append(a_dict)
            return value_list

        def import_function():
            """Returns food_dict with food name as keys and dictionaries of its characteristics as values."""
            in_list = create_value_dict()
            i = 0
            for d in the_list:
                value_dict = in_list[i]
                self.food_dict[the_list[i][food]] = value_dict
                i += 1
            return self.food_dict

        if isinstance(file, str):
            with open(file, newline="") as file:
                dict_obj = csv.DictReader(file)
                for row in dict_obj:
                    the_list.append(row)
                return import_function()
        else:
            dict_obj = csv.DictReader(file)
            for row in dict_obj:
                the_list.append(row)
            return import_function()

    def print_foods(self):
        i = 1
        for food in self.food_dict:
            print(f"{i}. {food}")
            i += 1

    def add_food_item(self, user_input):
        """Adds the water footprint of the food item in a list of food water footprints"""

        food = format_data(user_input, True)  # Formatting argument to number or changing it to lowercase and
        # removing spaces

        # If user input serial number of the food item from the list. This is for a commit.
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
            self.user_wfs.append(int(self.food_dict[food][self.unit]))
            self.user_foods.append(food)
            print(f"{food} added")
        except KeyError:
            print(f"{user_input} is out of range or not in our database. Maybe you misspelled?")

    def calculate_food_wf(self):
        """Calculates the total water footprint of the people in the household"""
        return f"Your water footprint is {sum(self.user_wfs) * self.household_members} in {self.unit}"

    def avg_compare(self):
        """ TODO: Create a method that compares the actual water footprint with the average and returns appropriate
        tips for each diet"""
        pass
