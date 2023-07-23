import csv
import re


def combine_keys_with_same_values(dictionary):
    new_dict = {}
    for key in dictionary:
        keys = []
        for key2 in dictionary:
            if dictionary[key] == dictionary[key2]:
                keys.append(key2)
        if len(keys) == 1:
            new_dict[key] = dictionary[key]
        else:
            new_dict[tuple(keys)] = dictionary[key]

    return new_dict


def format_data(data, replace_spaces):
    if replace_spaces:
        data = data.replace(" ", "")
    if data.isdigit():
        return int(data)
    else:
        parts = re.split(r"/", data)  # Split data using forward slash
        for part in parts:
            if "," in part:  # Check if any part contains a comma
                return ", ".join(parts)  # Join parts with a comma and a space
        return str(data).lower()


def create_value_dict(pros_keys, dict_list, replace_spaces):
    """Returns list of dictionaries with characteristics to be used as values for another dictionary"""
    value_list = []
    for d in dict_list:
        a_dict = {}
        for key in pros_keys:
            for k in d:
                if k == key or key == "Formatted":
                    break
            a_dict.update({key: format_data(d[k], replace_spaces)} if key is not None else {})
        value_list.append(a_dict)
    return value_list


class Water:
    def __init__(self, period, average=0, household_members=1):
        self.unit = ""
        self.period = period
        self.food_dict = {}  # Dictionary of Food with values being dicts themselves of characteristics
        self.average = average  # the value of average is stored here
        self.household_members = household_members
        self.user_foods = []  # All foods that the users added should be stored here
        self.user_wfs = []  # The water footprints of the users should be stored here. Sum is to be calculated from
        self.user_improvements = set({})  # This set has all tips for the user to improve their water footprint

    def import_food_csv(self, file, food, unit, serving=None, category=None, explanation=None, other=None):
        """Returns a list of dictionaries of food items and their characteristics as individual dictionaries"""

        self.unit = unit
        the_list = []
        foods_only = []

        def import_function():
            """Returns food_dict with food name as keys and dictionaries of its characteristics as values."""
            in_list = create_value_dict(["Formatted", serving, self.unit, category, explanation, other],
                                        the_list, True)
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
                foods_only.append(row[food])
            return import_function()

    def print_foods(self):
        i = 1
        for food in self.food_dict:
            print(f"{i}. {food}")
            i += 1

    def add_food_item(self, food, wf, times):
        """Adds the water footprint of the food item in a list of food water footprints"""
        self.user_wfs.append(wf * times)
        self.user_foods.append(food)
        print(f"{food} added")

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

    def calculate_food_wf(self):
        """Calculates the total water footprint of the people in the household"""
        return f"Your water footprint is {sum(self.user_wfs) * self.household_members} in {self.unit} per {self.period}."

    def display_tips(self, file, category, tip1, tip2=None, tip3=None, tip4=None, tip5=None):
        """Displays all applicable tips to improve the user's water footprints.
        IMPORTANT: argument for parameter (title of the csv file which has categories listed) should be same for all imported files"""
        tip_dicts = []  # To contain [{category:"", "tip1: "..}, {category: "", "tip1": ..}..]
        category_tips = {}  # To contain {category: {tip1: "", tip2: "" ..}..}
        obj = csv.DictReader(file)
        for row in obj:
            tip_dicts.append(row)
        value_dicts = create_value_dict([category, tip1, tip2, tip3, tip4, tip5], tip_dicts, False)
        i = 0
        for d in value_dicts:
            category_tips[tip_dicts[i][category]] = value_dicts[i]
            i += 1

        # To check all the tips that apply to the user through self.user_foods
        foods = {}
        for food in self.user_foods:
            for tip_category in category_tips:
                if self.food_dict[food][category] == format_data(tip_category, True):
                    foods[food] = category_tips[tip_category]

        self.user_improvements = combine_keys_with_same_values(foods)

        for key in self.user_improvements:
            print("\nSince you have added: ")
            if isinstance(key, tuple):
                for element in key:
                    print(f"• {element}")
            else:
                print(f"• {key}")

            print("\nKeep in mind the following:\n")

            for tip in [tip1, tip2, tip3, tip4, tip5]:
                if tip is not None:
                    the_tip = f" {self.user_improvements[key][tip]}"
                    if the_tip != "" and the_tip != " ":
                        print(f"- {self.user_improvements[key][tip]}")

    # TODO: Create an asking for explanations for the water footprint of each item that the user consumes.

    def avg_compare(self):
        """ TODO: Create a method that compares the actual water footprint with the average and returns appropriate
        tips for each diet"""
        pass
