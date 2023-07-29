import re
import csv


def import_csv(f):
    if isinstance(f, str):
        file = open(f)
    else:
        file = f
    return csv.DictReader(file)


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


def create_value_dict(pros_keys, dict_list, replace_spaces, formatted_title=None):
    """Returns list of dictionaries with characteristics to be used as values for another dictionary"""
    value_list = []
    for d in dict_list:
        a_dict = {}
        for key in pros_keys:
            for k in d:
                if k == key or key == formatted_title:
                    break
            # noinspection PyUnboundLocalVariable
            a_dict.update({key: format_data(d[k], replace_spaces)} if key is not None else {})
        value_list.append(a_dict)
    return value_list


class Food:
    def __init__(self, period, average=0, household_members=1):
        """
        Initialize the Food class.

        Parameters:
            period (str): The time period for which the water footprint is calculated (e.g., 'week', 'day').
            average (int or float, optional): The average value used in calculations.
            household_members (int, optional): The number of members in the household.
        """
        self.unit = ""
        self.period = period
        self.food_dict = {}  # Dictionary of Food with values being dicts themselves of characteristics
        self.average = average  # The value of average is stored here
        self.household_members = household_members
        self.user_foods = []  # All foods that the users added should be stored here
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
        """
        Add the water footprint of the food item to the list of food water footprints.

        Parameters:
            food (str): The name of the food item.
            wf (float): The water footprint of the food item.
            times (float): The number of times the food item is consumed.
        """
        self.user_wfs.append(wf * times)
        self.user_foods.append(food)
        print(f"{food} added")

    def calculate_food_wf(self):
        """
        Calculate the total water footprint of the people in the household.

        Returns:
            str: A string representing the calculated water footprint.
        """
        return f"Your water footprint is {sum(self.user_wfs) * self.household_members} in {self.unit} per {self.period}."


class Tips:
    def __init__(self, all_items_dict: dict, selected_items: list):
        """
        Initialize the Tips class.

        Parameters:
            all_items_dict (dict): A dictionary containing items as keys and dictionaries as values. Value dictionaries
            should have 'category' as a key, and the value should correspond to a category that exists in the file
            with tips of each category.
            selected_items (list): A list containing all the items that the user has selected.
        """
        self.category_column = ""
        self.category_tips_dict = {}  # To contain {category: {tip1: "", tip2: "" ..}..}
        self.all_items = all_items_dict
        self.selected_items = selected_items  # This list has all the user-selected items on which tips are applicable
        self.user_improvements = {}  # This dictionary has all tips for the user to improve their water footprint

    # noinspection PyIncorrectDocstring
    def import_tips(self, file, category, tip1, tip2=None, tip3=None, tip4=None, tip5=None):
        """
        Import tips from a CSV file.

        Parameters:
            file (str): The CSV file containing the tips.
            category (str): The title under which categories are stored in the file.
            tip1, tip2, tip3, tip4, tip5 (str): The titles under which the tips are stored.
        """
        tip_dicts = []  # To contain [{category:"", "tip1: "..}, {category: "", "tip1": ..}..]
        self.category_column = category
        obj = import_csv(file)
        for row in obj:
            tip_dicts.append(row)
        value_dicts = create_value_dict([tip1, tip2, tip3, tip4, tip5], tip_dicts, False)
        i = 0
        for _ in value_dicts:
            self.category_tips_dict[tip_dicts[i][category]] = value_dicts[i]
            i += 1

    def create_user_improvements(self, all_category=None):
        """
        Create user improvements based on the selected items.

        Parameters:
            all_category (str, optional): Title of the category where general tips are stored.
        """
        items = {}
        for item in self.selected_items:
            for tip_category in self.category_tips_dict:
                if self.all_items[item][self.category_column] == format_data(tip_category, True):
                    items[item] = self.category_tips_dict[tip_category]
        if all_category:
            items["all"] = self.category_tips_dict[all_category]

        self.user_improvements = combine_keys_with_same_values(items)

    def display_tips(self, message_before_tips=None, message_before_items=None, general_category=None,
                     general_message=None):
        """
        Display tips to the user.

        Parameters:
            message_before_tips (str, optional): The message to be displayed before printing tips of a category.
            message_before_items (str, optional): The message to be displayed before printing items of a category.
            general_category (str, optional): Title of the category where general tips are stored.
            general_message (str, optional): The message to be displayed before printing the general tips.
        """
        self.create_user_improvements(general_category)

        def print_tips(k, message=None):
            print(message) if isinstance(message, str) else print("\n")
            for tip in self.user_improvements[k]:
                the_tip = f" {self.user_improvements[k][tip]}"
                if the_tip != "" and the_tip != " ":
                    print(f"➢ {self.user_improvements[k][tip]}")

        if len(self.user_improvements) == 1:
            print("\nYour food choices have a reasonable water footprint. Keep up the good work!")
            print_tips(general_category, general_message)
        else:
            if message_before_items:
                for key in self.user_improvements:
                    if key == general_category:
                        message_before_tips = general_message
                    else:
                        print(message_before_items)
                        if isinstance(key, tuple):
                            for element in key:
                                print(f"• {element}")
                        else:
                            print(f"• {key}")
                    print_tips(key, message_before_tips)
            else:
                print(message_before_items)
                for key in self.user_improvements:
                    print_tips(key)


# Function to display a welcome message
def welcome_message():
    print("Welcome to the water footprint calculator!")
    print("This program is designed to give you an idea of how much water it takes to produce the foods you consume.")
    input("Press Enter to continue...")


# Function to get food data from CSV and create Food and Tips objects
def get_food_data():
    food_object = Food('week')
    tips_object = Tips(all_items_dict=food_object.food_dict, selected_items=food_object.user_foods)
    foods_dict = food_object.food_dict = food_object.load_food_csv("Water Footprint of Food Guide.csv", "Food", "Litres",
                                                                   serving="Serving Size", category="Category")
    return food_object, tips_object, foods_dict


# Function to display the list of food items
def display_food_items(food_object):
    print("Here is the list of food items: ")
    food_object.display_available_foods()


# Function to get user input for food consumption
def get_user_food_input(food_object):
    input_foods = []
    while True:
        user_input = input("""\nWhich foods from the list above do you consume? Type in the name or the serial number. 
        If you want to see the list again, type 'list'. 
        If you want to see all the items you have added, type 'my list'. 
        If you have finished entering foods, type 'end'. 
        Type here: """)

        food = format_data(user_input, True)
        if food == "list":
            display_food_items(food_object)
        elif food == "mylist":
            print(food_object.user_foods)
        elif food == "end":
            break
        else:
            items = food_object.check_food_item(user_input)
            if isinstance(items, dict):
                times = ""
                while not isinstance(times, float) and not isinstance(times, int):
                    times = input(f"How many times do you have {items['food']} per week, assuming the serving "
                                  f"size is {items['Serving Size']} ounces?: ")
                    try:
                        times = float(times)
                    except ValueError:
                        print(f"That is not a number. Please try again")
                food_object.add_food_item(items['food'], items['wf'], times)
                input_foods.append(items['food'])

    return input_foods


# Function to get user input for receiving tips
def get_tips_choice():
    return input(
        "Would you like some tips to improve your water footprint through better food habits? Type yes or no: ")


# Function to display tips based on user choices
if __name__ == "__main__":
    # Display welcome message
    welcome_message()

    # Get food data and create objects
    food_obj, food_tips_obj, foods = get_food_data()

    # Display food items to the user
    display_food_items(food_obj)

    # Get user input for food consumption
    user_foods = get_user_food_input(food_obj)

    # Calculate and display water footprint
    print(food_obj.calculate_food_wf())

    # Get user choice for tips
    want_tips = get_tips_choice()
    if want_tips.lower() == "yes":
        # Import and display tips
        food_tips_obj.import_tips("Tips for Categories.csv", "Category", "Tip1", "Tip2")
        food_tips_obj.display_tips(food_tips_obj, message_before_items="\nSince you have chosen:",
                                   general_category="all",
                                   general_message="\nHere are some general tips to keep in mind: ")

    input("\nThank you for using this water footprint calculator! Press Enter to exit: ")
