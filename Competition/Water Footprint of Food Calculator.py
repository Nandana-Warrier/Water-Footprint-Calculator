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
        return self.category_tips_dict

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


# noinspection SpellCheckingInspection
imported_food_data = {'Chocolate': {'Formatted': 'chocolate', 'Serving Size': 4, 'Litres': 1953, 'Category': 'other'},
                      'Almonds': {'Formatted': 'almonds', 'Serving Size': 4, 'Litres': 1828, 'Category': 'other'},
                      'Beef': {'Formatted': 'beef', 'Serving Size': 4, 'Litres': 1753, 'Category': 'meat'},
                      'Cashews': {'Formatted': 'cashews', 'Serving Size': 4, 'Litres': 1616, 'Category': 'other'},
                      'Pistachios': {'Formatted': 'pistachios', 'Serving Size': 4, 'Litres': 1291, 'Category': 'other'},
                      'Hazelnuts': {'Formatted': 'hazelnuts', 'Serving Size': 4, 'Litres': 1196, 'Category': 'other'},
                      'Lamb and mutton': {'Formatted': 'lambandmutton', 'Serving Size': 4, 'Litres': 1185,
                                          'Category': 'meat'},
                      'Walnuts': {'Formatted': 'walnuts', 'Serving Size': 4, 'Litres': 1056, 'Category': 'other'},
                      'Dried Apples': {'Formatted': 'driedapples', 'Serving Size': 4, 'Litres': 780,
                                       'Category': 'produce'},
                      'Prunes': {'Formatted': 'prunes', 'Serving Size': 4, 'Litres': 708, 'Category': 'produce'},
                      'Pork and bacon': {'Formatted': 'porkandbacon', 'Serving Size': 4, 'Litres': 681,
                                         'Category': 'meat'},
                      'Butter': {'Formatted': 'butter', 'Serving Size': 4, 'Litres': 632, 'Category': 'processedfoods'},
                      'Goat': {'Formatted': 'goat', 'Serving Size': 4, 'Litres': 628, 'Category': 'meat'},
                      'Quinoa': {'Formatted': 'quinoa', 'Serving Size': 4, 'Litres': 511, 'Category': 'other'},
                      'Dried Apricots': {'Formatted': 'driedapricots', 'Serving Size': 4, 'Litres': 503,
                                         'Category': 'produce'},
                      'Chicken': {'Formatted': 'chicken', 'Serving Size': 4, 'Litres': 492, 'Category': 'meat'},
                      'Turkey': {'Formatted': 'turkey', 'Serving Size': 4, 'Litres': 492, 'Category': 'meat'},
                      'Peanuts': {'Formatted': 'peanuts', 'Serving Size': 4, 'Litres': 450, 'Category': 'other'},
                      'Soy burger': {'Formatted': 'soyburger', 'Serving Size': 4, 'Litres': 428,
                                     'Category': 'processedfoods'},
                      'Figs': {'Formatted': 'figs', 'Serving Size': 4, 'Litres': 371, 'Category': 'produce'},
                      'Chicken Eggs': {'Formatted': 'chickeneggs', 'Serving Size': 4, 'Litres': 371,
                                       'Category': 'other'},
                      'Cows Milk': {'Formatted': 'cowsmilk', 'Serving Size': 4, 'Litres': 371,
                                    'Category': 'processedfoods'},
                      'Cheese': {'Formatted': 'cheese', 'Serving Size': 4, 'Litres': 360, 'Category': 'processedfoods'},
                      'Olives': {'Formatted': 'olives', 'Serving Size': 4, 'Litres': 341, 'Category': 'produce'},
                      'Chestnuts': {'Formatted': 'chestnuts', 'Serving Size': 4, 'Litres': 314, 'Category': 'other'},
                      'Oatmeal': {'Formatted': 'oatmeal', 'Serving Size': 4, 'Litres': 288,
                                  'Category': 'processedfoods'},
                      'Tofu': {'Formatted': 'tofu', 'Serving Size': 4, 'Litres': 288, 'Category': 'processedfoods'},
                      'Raisins': {'Formatted': 'raisins', 'Serving Size': 4, 'Litres': 276, 'Category': 'produce'},
                      'White Rice': {'Formatted': 'whiterice', 'Serving Size': 4, 'Litres': 276,
                                     'Category': 'processedfoods'},
                      'Apple juice': {'Formatted': 'applejuice', 'Serving Size': 8, 'Litres': 269,
                                      'Category': 'processedfoods'},
                      'Dates': {'Formatted': 'dates', 'Serving Size': 4, 'Litres': 257, 'Category': 'produce'},
                      'Black-eyed peas': {'Formatted': 'black-eyedpeas', 'Serving Size': 4, 'Litres': 254,
                                          'Category': 'produce'},
                      'Cowpeas': {'Formatted': 'cowpeas', 'Serving Size': 4, 'Litres': 254, 'Category': 'produce'},
                      'Coffee': {'Formatted': 'coffee', 'Serving Size': 8, 'Litres': 250, 'Category': 'processedfoods'},
                      'Plums': {'Formatted': 'plums', 'Serving Size': 4, 'Litres': 246, 'Category': 'produce'},
                      'Asparagus': {'Formatted': 'asparagus', 'Serving Size': 4, 'Litres': 246, 'Category': 'produce'},
                      'Brown Rice': {'Formatted': 'brownrice', 'Serving Size': 4, 'Litres': 246,
                                     'Category': 'processedfoods'},
                      'Soybeans': {'Formatted': 'soybeans', 'Serving Size': 4, 'Litres': 242, 'Category': 'produce'},
                      'Edamame': {'Formatted': 'edamame', 'Serving Size': 4, 'Litres': 242, 'Category': 'produce'},
                      'Milk': {'Formatted': 'milk', 'Serving Size': 8, 'Litres': 242, 'Category': 'processedfoods'},
                      'Orange juice': {'Formatted': 'orangejuice', 'Serving Size': 8, 'Litres': 242,
                                       'Category': 'processedfoods'},
                      'Lentils': {'Formatted': 'lentils', 'Serving Size': 4, 'Litres': 216, 'Category': 'produce'},
                      'Pasta': {'Formatted': 'pasta', 'Serving Size': 4, 'Litres': 212, 'Category': 'processedfoods'},
                      'Wheat flour': {'Formatted': 'wheatflour', 'Serving Size': 4, 'Litres': 208,
                                      'Category': 'processedfoods'},
                      'Guava': {'Formatted': 'guava', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce'},
                      'Mangoes': {'Formatted': 'mangoes', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce'},
                      'Pigeon peas': {'Formatted': 'pigeonpeas', 'Serving Size': 4, 'Litres': 204,
                                      'Category': 'produce'},
                      'Pizza; sauce and cheese': {'Formatted': 'pizza;sauceandcheese', 'Serving Size': 4, 'Litres': 201,
                                                  'Category': 'processedfoods'},
                      'Dry Beans': {'Formatted': 'drybeans', 'Serving Size': 4, 'Litres': 185, 'Category': 'produce'},
                      'Cherries': {'Formatted': 'cherries', 'Serving Size': 4, 'Litres': 182, 'Category': 'produce'},
                      'Plantains': {'Formatted': 'plantains', 'Serving Size': 4, 'Litres': 182, 'Category': 'produce'},
                      'Bread': {'Formatted': 'bread', 'Serving Size': 4, 'Litres': 182, 'Category': 'processedfoods'},
                      'Garbanzo beans': {'Formatted': 'garbanzobeans', 'Serving Size': 4, 'Litres': 155,
                                         'Category': 'produce'},
                      'Chickpeas': {'Formatted': 'chickpeas', 'Serving Size': 4, 'Litres': 155, 'Category': 'produce'},
                      'Apricots': {'Formatted': 'apricots', 'Serving Size': 4, 'Litres': 148, 'Category': 'produce'},
                      'Corn flour': {'Formatted': 'cornflour', 'Serving Size': 4, 'Litres': 144,
                                     'Category': 'processedfoods'},
                      'Sweet Corn': {'Formatted': 'sweetcorn', 'Serving Size': 4, 'Litres': 140, 'Category': 'produce'},
                      'Yogurt': {'Formatted': 'yogurt', 'Serving Size': 4, 'Litres': 136, 'Category': 'processedfoods'},
                      'Avocados': {'Formatted': 'avocados', 'Serving Size': 4, 'Litres': 132, 'Category': 'produce'},
                      'Wine': {'Formatted': 'wine', 'Serving Size': 5, 'Litres': 132, 'Category': 'other'},
                      'Crisps': {'Formatted': 'crisps', 'Serving Size': 4, 'Litres': 132, 'Category': 'processedfoods'},
                      'Potato chips': {'Formatted': 'potatochips', 'Serving Size': 4, 'Litres': 117,
                                       'Category': 'processedfoods'},
                      'Pears': {'Formatted': 'pears', 'Serving Size': 4, 'Litres': 106, 'Category': 'produce'},
                      'Peaches and Nectarines': {'Formatted': 'peachesandnectarines', 'Serving Size': 4, 'Litres': 102,
                                                 'Category': 'produce'},
                      'Soft drink': {'Formatted': 'softdrink', 'Serving Size': 8, 'Litres': 98,
                                     'Category': 'processedfoods'},
                      'Apples': {'Formatted': 'apples', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce'},
                      'Blueberries': {'Formatted': 'blueberries', 'Serving Size': 4, 'Litres': 95,
                                      'Category': 'produce'},
                      'Artichokes': {'Formatted': 'artichokes', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce'},
                      'Bananas': {'Formatted': 'bananas', 'Serving Size': 4, 'Litres': 91, 'Category': 'produce'},
                      'Tangerines': {'Formatted': 'tangerines', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce'},
                      'Clementines': {'Formatted': 'clementines', 'Serving Size': 4, 'Litres': 83,
                                      'Category': 'produce'},
                      'Mandarins': {'Formatted': 'mandarins', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce'},
                      'Broad beans': {'Formatted': 'broadbeans', 'Serving Size': 4, 'Litres': 76,
                                      'Category': 'produce'},
                      'Lemons': {'Formatted': 'lemons', 'Serving Size': 4, 'Litres': 72, 'Category': 'produce'},
                      'Limes': {'Formatted': 'limes', 'Serving Size': 4, 'Litres': 72, 'Category': 'produce'},
                      'Beer': {'Formatted': 'beer', 'Serving Size': 8, 'Litres': 72, 'Category': 'other'},
                      'Soy milk': {'Formatted': 'soymilk', 'Serving Size': 8, 'Litres': 72,
                                   'Category': 'processedfoods'},
                      'Grapes': {'Formatted': 'grapes', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce'},
                      'Garlic': {'Formatted': 'garlic', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce'},
                      'Fresh Peas': {'Formatted': 'freshpeas', 'Serving Size': '', 'Litres': 68, 'Category': 'produce'},
                      'Taro': {'Formatted': 'taro', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce'},
                      'Oranges': {'Formatted': 'oranges', 'Serving Size': 4, 'Litres': 64, 'Category': 'produce'},
                      'Okra': {'Formatted': 'okra', 'Serving Size': 4, 'Litres': 64, 'Category': 'produce'},
                      'Green Beans': {'Formatted': 'greenbeans', 'Serving Size': 4, 'Litres': 61,
                                      'Category': 'produce'},
                      'String beans': {'Formatted': 'stringbeans', 'Serving Size': 4, 'Litres': 61,
                                       'Category': 'produce'},
                      'Grapefruit': {'Formatted': 'grapefruit', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce'},
                      'Kiwifruit': {'Formatted': 'kiwifruit', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce'},
                      'Papaya': {'Formatted': 'papaya', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce'},
                      'Blackberries': {'Formatted': 'blackberries', 'Serving Size': 4, 'Litres': 45,
                                       'Category': 'produce'},
                      'Raspberries': {'Formatted': 'raspberries', 'Serving Size': 4, 'Litres': 45,
                                      'Category': 'produce'},
                      'Sweet potatoes': {'Formatted': 'sweetpotatoes', 'Serving Size': 4, 'Litres': 45,
                                         'Category': 'produce'},
                      'Cucumbers': {'Formatted': 'cucumbers', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce'},
                      'Eggplants': {'Formatted': 'eggplants', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce'},
                      'Chili Peppers': {'Formatted': 'chilipeppers', 'Serving Size': 4, 'Litres': 42,
                                        'Category': 'produce'},
                      'Sweet Peppers': {'Formatted': 'sweetpeppers', 'Serving Size': 4, 'Litres': 42,
                                        'Category': 'produce'},
                      'Strawberries': {'Formatted': 'strawberries', 'Serving Size': 4, 'Litres': 38,
                                       'Category': 'produce'},
                      'Pumpkins': {'Formatted': 'pumpkins', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce'},
                      'Squash': {'Formatted': 'squash', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce'},
                      'Broccoli': {'Formatted': 'broccoli', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce'},
                      'Brussels sprouts': {'Formatted': 'brusselssprouts', 'Serving Size': 4, 'Litres': 34,
                                           'Category': 'produce'},
                      'Cauliflower': {'Formatted': 'cauliflower', 'Serving Size': 4, 'Litres': 34,
                                      'Category': 'produce'},
                      'Potatoes': {'Formatted': 'potatoes', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce'},
                      'Spinach': {'Formatted': 'spinach', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce'},
                      'Cranberries': {'Formatted': 'cranberries', 'Serving Size': 4, 'Litres': 30,
                                      'Category': 'produce'},
                      'Pineapples': {'Formatted': 'pineapples', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
                      'Cabbage': {'Formatted': 'cabbage', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
                      'Kale': {'Formatted': 'kale', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
                      'Kohlrabi': {'Formatted': 'kohlrabi', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
                      'Onions': {'Formatted': 'onions', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
                      'Cantaloupe and other melons': {'Formatted': 'cantaloupeandothermelons', 'Serving Size': 4,
                                                      'Litres': 26, 'Category': 'produce'},
                      'Watermelons': {'Formatted': 'watermelons', 'Serving Size': 4, 'Litres': 26,
                                      'Category': 'produce'},
                      'Lettuce': {'Formatted': 'lettuce', 'Serving Size': 4, 'Litres': 26, 'Category': 'produce'},
                      'Tea': {'Formatted': 'tea', 'Serving Size': 8, 'Litres': 26, 'Category': 'other'},
                      'Carrots': {'Formatted': 'carrots', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'},
                      'Celery': {'Formatted': 'celery', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'},
                      'Tomatoes': {'Formatted': 'tomatoes', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'},
                      'Turnips': {'Formatted': 'turnips', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'}}

imported_tips_data = {'all': {
    'Tip1': 'Waste less:\n -  Because it takes a lot of water to get food to people’s plates, wasted food also means wasted water.\n -  The easiest and perhaps most effective thing to do is to plan out meals before heading to the store.',
    'Tip2': 'choose local food:\n - supporting local food production can help preserve water resources by keeping water usage for growing food within the local area. this reduces the need for transporting water across long distances.'
},
    'meat': {
        'Tip1': 'Choose Better Meat: Choose pasture raised meat as much as possible as despite negligible differences between water footprints, their impact on water resources are different:\n - Pasture-fed (Green Water Footprint): Uses forage as feed grown from rainwater and manure is used as fertilisers.\n - Conventional (Blue Water Footprint): Uses feed like corn that need irrigation and animal waste is turned into manure lagoons that can pollute surrounding waters.',
        'Tip2': 'Eat Less Meat: On average, the water footprint of a vegan or vegetarian is around half that of a meat eater. Eating less meat and replacing it with less water-intensive plant-based alternatives can reduce water footprints'
    },
    'produce': {
        'Tip1': "Choose Organic:\n - Organic farms usually don't use pesticides or synthetic fertilisers which could run off of farm fields and pollute nearby waters. \n - Soils at organic farms tend to be much better at retaining nutrients and moisture, which reduces the risk of groundwater pollution.\n - Buying products grown organically helps support farms that are making big efforts to reduce water pollution, which means those products have a smaller gray water footprint."
    },
    'processed foods': {
        'Tip1': 'In addition to growing the ingredients, processed foods require water for things like cleaning the food and machinery, pre-cooking the food, producing fuel for delivery and making packaging materials. Cutting back and replacing packaged foods with locally grown, organic alternatives can make a significant impact on your water footprint.'
    }}


# Function to display a welcome message
def welcome_message():
    print("Welcome to the water footprint calculator!")
    print("This program is designed to give you an idea of how much water it takes to produce the foods you consume.")
    input("Press Enter to continue...")


# Function to get food data from CSV and create Food and Tips objects
def get_food_data():
    food_object = Food('week')
    tips_object = Tips(all_items_dict=food_object.food_dict, selected_items=food_object.user_foods)
    foods_dict = food_object.food_dict = imported_food_data
    food_object.unit = "Litres"
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
        food_tips_obj.all_items = imported_food_data
        food_tips_obj.category_tips_dict = imported_tips_data
        food_tips_obj.category_column = "Category"
        food_tips_obj.display_tips(food_tips_obj, message_before_items="\nSince you have chosen:",
                                   general_category="all",
                                   general_message="\nHere are some general tips to keep in mind: ")

    input("\nThank you for using this water footprint calculator! Press Enter to exit: ")
