import csv


def import_csv(f):
    """Returns the file regardless of whether the argument is the file itself or the file name in the same folder."""
    if isinstance(f, str):
        file = open(f)
    else:
        file = f
    return csv.DictReader(file)


def combine_keys_with_same_values(dictionary):
    """Returns a new dictionary after combining keys with the same values into a single key-value pair using a tuple as the key."""
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


def format_data(data, replace_spaces, keep_case=False):
    """
    Formats data according to the needs of the Food, Tips classes.

        Parameters:
            data: The data to be formatted
            replace_spaces (bool): True to remove spaces of the formatted data, and False to keep the spacing.
            keep_case: True to keep the capitalization, False to change the formatted data to lowercase."""
    if replace_spaces:
        data = data.replace(" ", "")
    if data.isdigit():
        return int(data)
    else:
        if not keep_case:
            data = data.lower()
        if "/" in data:
            parts = tuple(data.split("/"))  # Split data using forward slash
            return parts
        return str(data)


def create_value_dict(prospective_keys, dict_list, replace_spaces, keep_case=False, formatted_title=None):
    """
    Returns list of dictionaries with characteristics to be used as values for another dictionary.

        Parameters:
            prospective_keys: The list of elements to be used as keys for each item in the value_dict. The order should be maintained.
            dict_list: The list of dictionaries from which the values for the value_dict are to be extracted. The keys should match the prospective keys, unless for formatted versions.
            replace_spaces: True to remove spaces of values, and False to keep the spacing.
            keep_case: True keep the capitalization in each value, False to change to lowercase.
            formatted_title: An extra key value pair in the value_dict, which is an formatted version of the key for identification purposes.
        """
    value_list = []
    for d in dict_list:
        a_dict = {}
        for key in prospective_keys:
            for k in d:
                if k == key or key == formatted_title:
                    break
            a_dict.update({key: format_data(d[k], replace_spaces, keep_case)} if key is not None else {})
        value_list.append(a_dict)
    return value_list


class Food:
    def __init__(self, period, household_members=1):
        """
        Initialize the Food class.

        Parameters:
            period (str): The time period for which the water footprint is calculated (e.g., 'week', 'day').
            household_members (int, optional): The number of members in the household.
        """
        # Keys of dictionaries in self.food_dict
        self.unit = ""  # Unit of water footprint (e.g., 'Litres' or 'Gallons')
        self.serving = None  # Title of the column containing serving size data
        self.category = None  # Title of the column containing food categories
        self.info = None  # Title of the column containing details of water footprints of food items
        self.other = None  # Title of an additional column containing other information

        self.period = period  # Time period for water footprint calculation
        self.food_dict = {}  # Dictionary of food items with dictionaries of characteristics as values
        self.household_members = household_members  # Number of members in the household
        self.user_foods = {}  # Dictionary to store user-added food items with their water footprints
        self.user_wfs = []  # List to store water footprints of user-added food items

    def load_food_csv(self, file, food, unit, serving=None, category=None, info=None, other=None):
        """
        Returns a list of dictionaries of food items and values being their characteristics as individual dictionaries.

        Parameters:
            file (str): The CSV file containing the food data.
            food (str): The title of the column containing food names.
            unit (str): The unit of water footprint (e.g., 'Litres' or 'Gallons').
            serving (str, optional): The title of the column containing serving size data.
            category (str, optional): The title of the column containing food categories.
            info (str, optional): The title of the column containing details of water footprints of food items.
            other (str, optional): The title of additional column containing other information.
        """
        # Set class variables to input values
        self.unit = unit
        self.serving = serving
        self.category = category
        self.info = info
        self.other = other

        the_list = []
        foods_only = []

        def import_function():
            """Returns food_dict with food name as keys and dictionaries of its characteristics as values."""
            in_list = create_value_dict(
                prospective_keys=["Formatted", self.serving, self.unit, self.category, self.other],
                dict_list=the_list, replace_spaces=True, formatted_title="Formatted")
            i = 0
            for _ in the_list:
                value_dict = in_list[i]
                if self.info:
                    value_dict[self.info] = the_list[i][self.info]
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

    def find_food_item(self, food):
        """
        Finds and returns the correct food item key based on user input.

        Parameters:
            food (str or int): The user input for food item (name or serial number).
        """
        if isinstance(food, int):
            i = 1
            for f in self.food_dict:
                if i == food:
                    food = f
                    break
                i += 1
        else:
            food = format_data(food, True)
            for f in self.food_dict:
                if self.food_dict[f]["Formatted"] == food:
                    food = f
        return food

    def check_food_item(self, user_input):
        """
        Check if the user input corresponds to a valid food item and returns dictionary containing the food name, water footprint, and serving size.

        Parameters:
            user_input (str or int): The user input for food item (name or serial number).
        """
        food = user_input
        food = format_data(food, True)  # Formatting argument to number or changing it to lowercase and removing spaces

        food = self.find_food_item(food)

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
        print(f"\n{food} added. ")

    def print_info(self, food):
        """
        Print information about a food item.

        Parameters:
            food (str): The name of the food item.
        """
        return self.food_dict[food][self.info]

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
        value_dicts = create_value_dict(prospective_keys=[tip1, tip2, tip3, tip4, tip5], dict_list=tip_dicts,
                                        replace_spaces=False, keep_case=True)
        i = 0
        for _ in value_dicts:
            self.category_tips_dict[tip_dicts[i][category]] = value_dicts[i]
            i += 1
        return self.category_tips_dict

    def create_user_improvements(self, item_key, all_category=None):
        """
        Create user improvements based on the selected items.

        Parameters:
            item_key (str): The key for the item or tuple of items for the value dict of each category.
                            self.user_improvements[category][item_key] = item or (item1, item2, item3)
            all_category (str, optional): Title of the category where general tips are stored.
        """
        for tip_category in self.category_tips_dict:
            value_dict = {}
            item_key_list = []
            if tip_category == all_category:
                item_key_list = self.selected_items
            else:
                for item in self.selected_items:
                    item_category = self.all_items[item][self.category_column]
                    if format_data(tip_category, True) == item_category or format_data(tip_category,
                                                                                       True) in item_category:
                        item_key_list.append(item)
            if len(item_key_list) != 0:
                value_dict[item_key] = tuple(item_key_list)
                value_dict['Tips'] = self.category_tips_dict[tip_category]
                self.user_improvements[tip_category] = value_dict

    def display_tips(self, item_key, message_before_tips=None, message_before_items=None, general_category=None,
                     general_message=None):
        """
        Display tips to the user.

        Parameters:
            message_before_tips (str, optional): The message to be displayed before printing tips of a category.
            message_before_items (str, optional): The message to be displayed before printing items of a category.
            general_category (str, optional): Title of the category where general tips are stored.
            general_message (str, optional): The message to be displayed before printing the general tips.
            item_key : The key to be used to fetch all the items belonging to a category in the user_improvements dictionary.
        """
        self.create_user_improvements(item_key=item_key, all_category=general_category)

        def print_tips(k, message=None):
            print(message) if isinstance(message, str) else print("")
            for tip in self.user_improvements[k]['Tips']:
                the_tip = f" {self.user_improvements[k]['Tips'][tip]}"
                if the_tip != "" and the_tip != " ":
                    print(f"➢ {self.user_improvements[k]['Tips'][tip]}")

        if message_before_items:
            for key in self.user_improvements:
                if key == general_category:
                    continue
                else:
                    print(message_before_items)
                    for element in self.user_improvements[key][item_key]:
                        print(f"• {element}")
                print_tips(key, message_before_tips)
            print_tips(general_category, general_message)
        else:
            for key in self.user_improvements:
                print_tips(key)


# DATA

food_dict = {'Chocolate': {'Formatted': 'chocolate', 'Serving Size': 4, 'Litres': 1953, 'Category': 'other',
                           'Information': 'The water footprint of chocolate varies depending on where and how the cocoa (or cacao) trees and other ingredients were grown. Chocolate ingredients are almost entirely rainfed (green water), receive little irrigation (blue water) and require some fertilizer and pesticides that cause water pollution (grey water). There is also water pollution associated with processing, packaging and transporting chocolate.'},
             'Almonds': {'Formatted': 'almonds', 'Serving Size': 4, 'Litres': 1828, 'Category': 'other',
                         'Information': 'Almond trees thrive in semi-arid Mediterranean climates, are primarily rainfed (green water), can require significant amounts of irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Beef': {'Formatted': 'beef', 'Serving Size': 4, 'Litres': 1753, 'Category': 'meat',
                      'Information': "Cattle tend to have long lives and eat large amounts of grass and/or grain. Most US cattle eat grass for the majority of their lives and are finished in feedlots where they are given feed made from corn, hay and leftover distiller's grain. These crops are predominantly rainfed (green water), however feed grain crops are increasingly being irrigated (blue water). Beef production can cause water pollution (grey water) from large concentrations of manure leaching into soil and from fertilizer and/or pesticides used to grow feed crops running off into waterways."},
             'Cashews': {'Formatted': 'cashews', 'Serving Size': 4, 'Litres': 1616, 'Category': 'other',
                         'Information': 'Cashew trees are tropical evergreens that rely almost entirely on rainfall (green water) and can receive supplemental irrigation (blue water).'},
             'Pistachios': {'Formatted': 'pistachios', 'Serving Size': 4, 'Litres': 1291, 'Category': 'other',
                            'Information': 'Pistachio trees grow in warm, Mediterranean climates where they are primarily irrigated (blue water) in addition to being rainfed (green water), and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Hazelnuts': {'Formatted': 'hazelnuts', 'Serving Size': 4, 'Litres': 1196, 'Category': 'other',
                           'Information': 'Hazelnuts grow on shrubs or as single-stem trees in moderate climates where they are mainly rainfed (green water), can require a significant amount of irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Lamb and mutton': {'Formatted': 'lambandmutton', 'Serving Size': 4, 'Litres': 1185, 'Category': 'meat',
                                 'Information': 'Most sheep are raised in pasture- and forage-based systems and eat grass that is predominantly rainfed (green water), although sometimes they are fed grain in feedlots. Feed grains are typically rainfed (green water) but are increasingly being irrigated (blue water). Because of the foraging diet of sheep and lambs, their production tends to cause minimal water pollution (grey water).'},
             'Walnuts': {'Formatted': 'walnuts', 'Serving Size': 4, 'Litres': 1056, 'Category': 'other',
                         'Information': 'Walnut trees thrive in semi-arid Mediterranean climates, are primarily rainfed (green water), can require significant amounts of irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Dried Apples': {'Formatted': 'driedapples', 'Serving Size': 4, 'Litres': 780, 'Category': 'driedfruits',
                              'Information': 'Apple trees are primarily rainfed (green water) and can receive supplemental irrigation (blue water). Most apple trees are treated heavily with pesticides, and can cause water pollution (grey water) from fertilizer and/or pesticide use. \n- Dried fruits tend to have bigger water footprints than their fresh variety because of water consumption associated with processing.'},
             'Prunes': {'Formatted': 'prunes', 'Serving Size': 4, 'Litres': 708, 'Category': 'driedfruits',
                        'Information': 'Plum trees thrive in a warm Mediterranean climate and are primarily rainfed (green water), can receive some supplemental irrigation (blue water) and can cause water pollution from the significant application of fertilizer and/or pesticides (grey water). \n- Dried fruits tend to have bigger water footprints than their fresh variety because of water consumption associated with processing.'},
             'Pork and bacon': {'Formatted': 'porkandbacon', 'Serving Size': 4, 'Litres': 681, 'Category': 'meat',
                                'Information': 'Most hogs are raised in "industrial" systems, in feedlots where they are fed grain made from wheat, corn, barley, oats and sorghum, although in the US the feed is often made from corn and soybeans. Feed grains are primarily rainfed (green water) but are increasingly being irrigated (blue water). Pork production can cause water pollution (grey water) from large concentrations of animal manure leaching into soils and from the fertilizer and/or pesticides used to grow feed crops running off into waterways.'},
             'Butter': {'Formatted': 'butter', 'Serving Size': 4, 'Litres': 632, 'Category': 'processedfoods',
                        'Information': 'Dairy cows tend to have long lives in systems where they eat large quantities of grass and feed grain made from corn and soybeans.\nDairies can also cause a significant amount of water pollution from manure leaching into waterways.\n- Feed grains are predominantly rainfed (green water), although corn and soybeans are increasingly being irrigated (blue water) in some states. Butter production can cause water pollution (grey water) from processing, packaging and transportation, and when fertilizer and/or pesticides are used in feed crop production.'},
             'Goat': {'Formatted': 'goat', 'Serving Size': 4, 'Litres': 628, 'Category': 'meat',
                      'Information': 'Most meat goats are raised in pasture- and forage-based systems and eat grass that is predominantly rainfed (green water) and can receive some small amount of irrigation (blue water). Because of the foraging diet of meat goats, their production tends to cause minimal water pollution (grey water).'},
             'Quinoa': {'Formatted': 'quinoa', 'Serving Size': 4, 'Litres': 511, 'Category': 'other',
                        'Information': 'Native to the semi-arid Andes Mountains, quinoa plants are almost entirely rainfed (green water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Dried Apricots': {'Formatted': 'driedapricots', 'Serving Size': 4, 'Litres': 503,
                                'Category': 'driedfruits',
                                'Information': 'Apricot trees are primarily rainfed (green water), but receive significant amounts of irrigation (blue water) as they are typically produced in semi-arid regions. \n- Dried fruits tend to have bigger water footprints than their fresh variety because of water consumption associated with processing.'},
             'Chicken': {'Formatted': 'chicken', 'Serving Size': 4, 'Litres': 492, 'Category': 'meat',
                         'Information': 'Most chickens in the US are raised in "industrial" systems where they\'re given feed made from corn and soybeans. Most feed grains are rainfed (green water) but are increasingly being irrigated (blue water). Chicken production can cause water pollution (grey water) from large concentrations of animal manure leaching into soil and from fertilizer and/or pesticides used to grow feed crops leaching into waterways.'},
             'Turkey': {'Formatted': 'turkey', 'Serving Size': 4, 'Litres': 492, 'Category': 'meat',
                        'Information': 'Most turkeys in the US are raised in "industrial" systems where they are given feed made from corn and soybeans. Feed grains are primarily rainfed (green water) but are also increasingly being irrigated (blue water). Turkey production can cause water pollution (grey water) from large concentrations of animal manure leaching into the soil and from the fertilizer and/or pesticides used to grow feed crops running off into waterways.'},
             'Peanuts': {'Formatted': 'peanuts', 'Serving Size': 4, 'Litres': 450, 'Category': 'other',
                         'Information': 'Peanut plants rely almost entirely on rainfall (green water), can receive some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Soy burger': {'Formatted': 'soyburger', 'Serving Size': 4, 'Litres': 428, 'Category': 'processedfoods',
                            'Information': 'Veggie burgers can be made from many different ingredients; soy is used here as a stand-in. The water footprint is primarily associated with growing soybeans and other ingredients (spices, binders, etc.) required to make the burger. \n- Soybeans are mostly rainfed (green water), although in the US they are increasingly being irrigated (blue water) in some states and can cause pollution (grey water) from fertilizer and/or pesticides used to grow the soybeans and other ingredients.\n- There is also pollution associated with manufacturing veggie burgers, including processing, assembly, packaging and transportation.'},
             'Figs': {'Formatted': 'figs', 'Serving Size': 4, 'Litres': 371, 'Category': 'produce',
                      'Information': 'Fig trees thrive in a Mediterranean climate and require regular and substantial irrigation (blue water) to augment the rain (green water) they receive.'},
             'Chicken Eggs': {'Formatted': 'chickeneggs', 'Serving Size': 4, 'Litres': 371, 'Category': 'other',
                              'Information': 'In the US, most layer chickens that produce eggs are raised in "industrial" systems where they\'re given feed made from corn and soybeans. Most feed grains are rainfed (green water) but are increasingly being irrigated (blue water). Chicken (egg) production can cause water pollution (grey water) from large concentrations of animal manure leaching into the soil and from the fertilizer and/or pesticides used to grow feed crops leaching into waterways.'},
             'Cheese': {'Formatted': 'cheese', 'Serving Size': 4, 'Litres': 360,
                        'Category': ('processedfoods', 'dairy'),
                        'Information': 'Cheese production can cause pollution (grey water) because of processing, packaging and transportation, and when fertilizer and/or pesticides are used in feed crop production.\n- Dairy cows tend to have long lives in systems where they eat large quantities of grass and feed grain made from corn and soybeans. Feed grains are predominantly rainfed (green water), although in the US, corn and soybean plants are increasingly being irrigated (blue water) in some states. \n- Dairies can also cause a significant amount of water pollution from manure leaching into waterways.'},
             'Olives': {'Formatted': 'olives', 'Serving Size': 4, 'Litres': 341, 'Category': 'produce',
                        'Information': 'Olive trees grow in warm, Mediterranean climates where they are mainly rainfed (green water) and can require a significant amount of irrigation (blue water).'},
             'Chestnuts': {'Formatted': 'chestnuts', 'Serving Size': 4, 'Litres': 314, 'Category': 'other',
                           'Information': 'Chestnut trees rely largely on rainfall (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Oatmeal': {'Formatted': 'oatmeal', 'Serving Size': 4, 'Litres': 288,
                         'Category': ('processedfoods', 'milledflour'),
                         'Information': 'Oat plants are primarily rainfed (green water), can receive some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).\n- Milled oats (like oatmeal) tend to have bigger water footprints than their primary crop because of water consumption associated with processing. '},
             'Tofu': {'Formatted': 'tofu', 'Serving Size': 4, 'Litres': 288, 'Category': 'processedfoods',
                      'Information': 'The water footprint of tofu is largely associated with growing soybeans. \n- Soybeans are mostly rainfed (green water), although in the US, soybeans are increasingly being irrigated (blue water) in some states. There is also pollution (grey water) associated with processing, packaging and transporting tofu, and a grey water component from fertilizer and/or pesticide use in growing soybeans.'},
             'Raisins': {'Formatted': 'raisins', 'Serving Size': 4, 'Litres': 276, 'Category': 'driedfruits',
                         'Information': 'Grapes vines are primarily rainfed (green water), can require supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'White Rice': {'Formatted': 'whiterice', 'Serving Size': 4, 'Litres': 276, 'Category': 'processedfoods',
                            'Information': 'Rice plants are rainfed (green water) although most rice produced in the US is irrigated or grown in flooded fields (blue water), and it can cause water pollution from the application of fertilizer and/or pesticides (grey water).\n- Like brown rice, white rice has the hull removed as well as the bran, which increases its water footprint compared to brown rice because of extra processing. '},
             'Apple juice': {'Formatted': 'applejuice', 'Serving Size': 8, 'Litres': 269, 'Category': 'processedfoods',
                             'Information': 'The water footprint of apple juice varies depending on where and how the apples were grown. Most of the water footprint is associated with growing apple trees which are primarily rainfed (green water) and are supplemented with substantial amounts of irrigation (blue water) in drier regions. Apple trees are treated heavily with pesticides, and can cause water pollution (grey water) from fertilizer and/or pesticide use. There is also pollution associated with processing, packaging and transporting juice.'},
             'Dates': {'Formatted': 'dates', 'Serving Size': 4, 'Litres': 257, 'Category': 'produce',
                       'Information': 'Date palm trees thrive in hot, arid climates and require regular irrigation (blue water) to augment the little rain (green water) they typically receive.'},
             'Black-eyed peas': {'Formatted': 'black-eyedpeas', 'Serving Size': 4, 'Litres': 254, 'Category': 'produce',
                                 'Information': 'Cowpeas include black-eyed peas and are a warm season, drought-resistant crop. Cowpea plants are primarily rainfed (green water), receive little supplemental irrigation (blue water) although irrigation will increase their productivity, and are typically grown without pesticides.'},
             'Cowpeas': {'Formatted': 'cowpeas', 'Serving Size': 4, 'Litres': 254, 'Category': 'produce',
                         'Information': 'Cowpeas include black-eyed peas and are a warm season, drought-resistant crop. Cowpea plants are primarily rainfed (green water), receive little supplemental irrigation (blue water) although irrigation will increase their productivity, and are typically grown without pesticides.'},
             'Coffee': {'Formatted': 'coffee', 'Serving Size': 8, 'Litres': 250, 'Category': 'processedfoods',
                        'Information': 'Coffee trees are rainfed (green water) if they are shade-grown and receive significant irrigation (blue water) if they are sun-grown. They can cause water pollution from the use of fertilizer and/or pesticides (grey water) and there is a significant amount of water used in processing coffee using the wet washing method (it can also be "dry washed"). There is also pollution associated with processing, packaging and transporting coffee.'},
             'Plums': {'Formatted': 'plums', 'Serving Size': 4, 'Litres': 246, 'Category': 'produce',
                       'Information': 'Plum trees thrive in a warm Mediterranean climate and are primarily rainfed (green water), can receive some supplemental irrigation (blue water) and can cause water pollution from the significant application of fertilizer and/or pesticides (grey water).'},
             'Asparagus': {'Formatted': 'asparagus', 'Serving Size': 4, 'Litres': 246, 'Category': 'produce',
                           'Information': 'Asparagus plants are primarily rainfed (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Brown Rice': {'Formatted': 'brownrice', 'Serving Size': 4, 'Litres': 246, 'Category': 'processedfoods',
                            'Information': 'Brown rice has the hull or husk removed, which increases its water footprint for processing. Rice is rainfed (green water) although most rice in the US is irrigated or grown in flooded fields (blue water), and it can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Soybeans': {'Formatted': 'soybeans', 'Serving Size': 4, 'Litres': 242, 'Category': 'produce',
                          'Information': 'Soybeans that are grown to be eaten as food, like edamame, are a small percentage of total production. Most of the crop is grown to be heavily processed for by-products like soybean oil and meal. Soybeans plants are primarily rainfed (green water), but depending on the type of soybean and the soil conditions, they can receive supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Edamame': {'Formatted': 'edamame', 'Serving Size': 4, 'Litres': 242, 'Category': 'produce',
                         'Information': 'Soybeans that are grown to be eaten as food, like edamame, are a small percentage of total production. Most of the crop is grown to be heavily processed for by-products like soybean oil and meal. Soybeans plants are primarily rainfed (green water), but depending on the type of soybean and the soil conditions, they can receive supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Milk': {'Formatted': 'milk', 'Serving Size': 8, 'Litres': 242, 'Category': 'dairy',
                      'Information': 'Dairy cows tend to have long lives in systems where they eat large quantities of grass and feed grains, both of which are predominantly rainfed (green water). In the US, feed grains are increasingly being irrigated (blue water) in some states and can cause water pollution (grey water) from fertilizer and/or pesticide use. Dairies can also pollute water (grey water) when concentrated animal manure leaches into waterways, and there is pollution associated with processing, packaging and transporting milk.'},
             'Orange juice': {'Formatted': 'orangejuice', 'Serving Size': 8, 'Litres': 242,
                              'Category': 'processedfoods',
                              'Information': 'The water footprint of orange juice is mainly associated with growing oranges and varies depending on where and how the oranges were grown. Orange trees are primarily rainfed (green water), can require supplemental irrigation (blue water) and can cause pollution from the use of fertilizer and pesticides (grey water). The grey water footprint is primarily associated with processing, packaging and transporting orange juice.'},
             'Lentils': {'Formatted': 'lentils', 'Serving Size': 4, 'Litres': 216, 'Category': 'produce',
                         'Information': 'Lentil vines are primarily a dryland, rainfed (green water) crop, but can receive supplemental irrigation (blue water) which can increase problems with pests, and can cause a significant amount of water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Pasta': {'Formatted': 'pasta', 'Serving Size': 4, 'Litres': 212,
                       'Category': ('processedfoods', 'milledflour'),
                       'Information': 'Dry pasta is made from specially milled wheat flour. The water footprint of pasta varies depending on where and how the wheat plants were grown. Wheat is primarily rainfed (green water) and can receive supplemental irrigation (blue water). There is pollution (grey water) associated with fertilizer and/or pesticide use in growing wheat as well as with processing, packaging and transporting wheat flour and pasta.'},
             'Wheat flour': {'Formatted': 'wheatflour', 'Serving Size': 4, 'Litres': 208,
                             'Category': ('processedfoods', 'milledflour'),
                             'Information': 'Milled flours tend to have bigger water footprints than their primary crop (i.e., wheat) because of water consumption associated with processing. Wheat is primarily rainfed (green water), can require some supplemental irrigation (blue water) and can cause water pollution from application of fertilizer and pesticides (grey water).'},
             'Guava': {'Formatted': 'guava', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce',
                       'Information': 'Guava trees are mainly rainfed (green water), can require some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Mangoes': {'Formatted': 'mangoes', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce',
                         'Information': 'Mango trees are mainly rainfed (green water), can require supplemental irrigation (blue water) although they need a dry period to flower, and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Pigeon peas': {'Formatted': 'pigeonpeas', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce',
                             'Information': 'Pigeon pea shrubs are a significant warm weather, drought-resistant crop that can be grown in poor soils and are primarily rainfed (green water). They can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Pizza; sauce and cheese': {'Formatted': 'pizza;sauceandcheese', 'Serving Size': 4, 'Litres': 201,
                                         'Category': 'processedfoods',
                                         'Information': 'Pizza is made and eaten worldwide, and the water footprint varies depending on where and how the ingredients were produced. The water footprint comes from the rainfall (green water) and irrigation (blue water) requirements associated with growing wheat for the crust, tomatoes for the sauce, as well as grass and grains to feed the cows that provide milk for the cheese (which contributes the most). There is also water pollution (grey water) that comes from growing and processing the ingredients and processing, packaging and transporting the pizzas.'},
             'Dry Beans': {'Formatted': 'drybeans', 'Serving Size': 4, 'Litres': 185, 'Category': 'produce',
                           'Information': 'Dry beans are grown on bushes or vines and are primarily rainfed (green water), but in the US they receive supplemental irrigation (blue water) and can cause a lot of water pollution from the use of pesticides (grey water).'},
             'Cherries': {'Formatted': 'cherries', 'Serving Size': 4, 'Litres': 182, 'Category': 'produce',
                          'Information': 'Cherry trees are mainly rainfed (green water), can receive substantial irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Plantains': {'Formatted': 'plantains', 'Serving Size': 4, 'Litres': 182, 'Category': 'produce',
                           'Information': 'Plantains and bananas are related. Plantain trees are almost entirely rainfed (green water) and receive very little irrigation (blue water).'},
             'Bread': {'Formatted': 'bread', 'Serving Size': 4, 'Litres': 182, 'Category': 'processedfoods',
                       'Information': 'The water footprint of bread varies depending on where and how the wheat plants were grown. Wheat is primarily rainfed (green water) and can receive supplemental irrigation (blue water). There is water pollution (grey water) associated with fertilizer and/or pesticide use in growing wheat, and there is water pollution associated with processing, packaging and transporting wheat flour and bread.'},
             'Garbanzo beans': {'Formatted': 'garbanzobeans', 'Serving Size': 4, 'Litres': 155, 'Category': 'produce',
                                'Information': 'Chickpea plants are a cool season, drought-tolerant crop that are primarily rainfed (green water), can receive some supplemental irrigation (blue water) in drier areas and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Chickpeas': {'Formatted': 'chickpeas', 'Serving Size': 4, 'Litres': 155, 'Category': 'produce',
                           'Information': 'Chickpea plants are a cool season, drought-tolerant crop that are primarily rainfed (green water), can receive some supplemental irrigation (blue water) in drier areas and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Apricots': {'Formatted': 'apricots', 'Serving Size': 4, 'Litres': 148, 'Category': 'produce',
                          'Information': 'Apricot trees are primarily rainfed (green water), but receive significant amounts of irrigation (blue water) as they are typically produced in semi-arid regions.'},
             'Corn flour': {'Formatted': 'cornflour', 'Serving Size': 4, 'Litres': 144, 'Category': 'processedfoods',
                            'Information': 'Corn plants are primarily rainfed (green water), are the most heavily irrigated crop (blue water) in the US and can cause significant water pollution from the heavy application of fertilizer and/or pesticides (grey water).'},
             'Sweet Corn': {'Formatted': 'sweetcorn', 'Serving Size': 4, 'Litres': 140, 'Category': 'produce',
                            'Information': 'Corn is the most irrigated crop in the US because irrigation significantly increases corn yields. Corn plants are primarily rainfed (green water), receive significant supplemental irrigation (blue water) and cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Yogurt': {'Formatted': 'yogurt', 'Serving Size': 4, 'Litres': 136,
                        'Category': ('processedfoods', 'dairy'),
                        'Information': 'Dairy cows tend to have long lives in systems where they eat large quantities of grass and feed grain made from corn and soybeans. Feed grains are predominantly rainfed (green water), although in the US, corn and soybeans are increasingly being irrigated (blue water) in some states. Yogurt production can cause pollution (grey water) because of processing, packaging and transportation, and when fertilizer and/or pesticides are used to grow grains for feed. Dairies can also cause a significant amount of water pollution from manure leaching into waterways.'},
             'Avocados': {'Formatted': 'avocados', 'Serving Size': 4, 'Litres': 132, 'Category': 'produce',
                          'Information': 'Avocado trees are primarily rainfed (green water), require a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Wine': {'Formatted': 'wine', 'Serving Size': 5, 'Litres': 132, 'Category': 'processedfoods',
                      'Information': 'The water footprint is mainly associated with growing the grapes and varies depending on where and how the grapes were grown. Grape vines are primarily rainfed (green water), can receive significant supplemental irrigation (blue water) and can cause pollution from the use of fertilizer and/or pesticides (grey water). The grey water footprint is primarily associated with processing, packaging and transporting wine.'},
             'Crisps': {'Formatted': 'crisps', 'Serving Size': 4, 'Litres': 132, 'Category': 'processedfoods',
                        'Information': 'Potatoes are a root crop that is primarily rainfed (green water) and can receive supplemental irrigation (blue water). There is pollution (grey water) associated with fertilizer and/or pesticide use in producing potatoes and other ingredients as well as with processing, packaging and transporting potato chips.'},
             'Potato chips': {'Formatted': 'potatochips', 'Serving Size': 4, 'Litres': 117,
                              'Category': 'processedfoods',
                              'Information': 'Potatoes are a root crop that is primarily rainfed (green water) and can receive supplemental irrigation (blue water). There is pollution (grey water) associated with fertilizer and/or pesticide use in producing potatoes and other ingredients as well as with processing, packaging and transporting potato chips.'},
             'Pears': {'Formatted': 'pears', 'Serving Size': 4, 'Litres': 106, 'Category': 'produce',
                       'Information': 'Pear trees are primarily rainfed (green water) and receive some supplemental irrigation (blue water) as well as significant fertilizer and pesticides (grey water).'},
             'Peaches and Nectarines': {'Formatted': 'peachesandnectarines', 'Serving Size': 4, 'Litres': 102,
                                        'Category': 'produce',
                                        'Information': 'Peach and nectarine trees are mainly rainfed (green water), receive supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Soft drink': {'Formatted': 'softdrink', 'Serving Size': 8, 'Litres': 98, 'Category': 'processedfoods',
                            'Information': 'Sugar-sweetened sodas are produced worldwide and in most US states either by major manufacturers or craft producers. Production includes combining sugar and flavorings to create the soft drink. The water footprint is mainly associated with the sugar used (primarily sugar beets, but also sugar cane and corn sugar) and varies depending on where and how the sugar was grown. Sugar beet plants are primarily rainfed (green water), can receive significant supplemental irrigation (blue water) and can cause pollution from the use of fertilizer and pesticides (grey water). The grey water footprint is primarily associated with processing, packaging and transporting the ingredients.'},
             'Apples': {'Formatted': 'apples', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce',
                        'Information': 'Apple trees are primarily rainfed (green water) and can receive supplemental irrigation (blue water). Most apple trees are treated heavily with pesticides, and can cause water pollution (grey water) from fertilizer and/or pesticide use.'},
             'Blueberries': {'Formatted': 'blueberries', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce',
                             'Information': 'Blueberry bushes tend to receive equal amounts of water from rain (green water) and irrigation (blue water), and can cause water pollution from the application of fertilizer and/or pesticides (grey water'},
             'Artichokes': {'Formatted': 'artichokes', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce',
                            'Information': 'Artichoke plants are primarily rainfed (green water), require a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Bananas': {'Formatted': 'bananas', 'Serving Size': 4, 'Litres': 91, 'Category': 'produce',
                         'Information': 'Banana trees are primarily rainfed (green water) and can receive supplemental irrigation (blue water).'},
             'Tangerines': {'Formatted': 'tangerines', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce',
                            'Information': 'Trees are primarily rainfed (green water), can require some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Clementines': {'Formatted': 'clementines', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce',
                             'Information': 'Trees are primarily rainfed (green water), can require some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Mandarins': {'Formatted': 'mandarins', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce',
                           'Information': 'Trees are primarily rainfed (green water), can require some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Broad beans': {'Formatted': 'broadbeans', 'Serving Size': 4, 'Litres': 76, 'Category': 'produce',
                             'Information': 'Fava bean plants are primarily rainfed (green water), under dry conditions require a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Lemons': {'Formatted': 'lemons', 'Serving Size': 4, 'Litres': 72, 'Category': 'produce',
                        'Information': 'Lemon trees are mainly rainfed (green water), can receive some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Limes': {'Formatted': 'limes', 'Serving Size': 4, 'Litres': 72, 'Category': 'produce',
                       'Information': 'Lime trees are mainly rainfed (green water), can receive some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Beer': {'Formatted': 'beer', 'Serving Size': 8, 'Litres': 72, 'Category': 'processedfoods',
                      'Information': 'Specific types of barley plants are used for malt production and most malt is used for brewing beer. Most of the water footprint of beer is associated with growing barley. The water footprint of beer varies depending on where and how barley was grown. Barley is primarily rainfed (green water), can be supplemented with irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water). There is also pollution associated with processing, packaging and transporting beer.'},
             'Soy milk': {'Formatted': 'soymilk', 'Serving Size': 8, 'Litres': 72, 'Category': 'processedfoods',
                          'Information': 'The water footprint is mainly associated with growing soybeans. Soybean plants are primarily rainfed (green water), are increasingly being irrigated in the US (blue water) and can cause pollution from the use of fertilizer and/or pesticides (grey water). The grey water footprint is primarily associated with processing, packaging and transporting soy milk.'},
             'Grapes': {'Formatted': 'grapes', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce',
                        'Information': 'Grape vines rely mainly on rainfall (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Garlic': {'Formatted': 'garlic', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce',
                        'Information': 'Garlic root bulbs are rainfed (green water), can require a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Fresh Peas': {'Formatted': 'freshpeas', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce',
                            'Information': 'Green peas are rainfed (green water), receive a significant amount of supplemental irrigation water (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Taro': {'Formatted': 'taro', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce',
                      'Information': 'Taro root is one of the oldest cultivated crops, and when dryland farmed, it is rainfed (green water). Hawaiian taro cultivation uses flooded field and wetland techniques, which increase the blue water requirements. Taro production can cause water pollution from the use of pesticides (grey water).'},
             'Oranges': {'Formatted': 'oranges', 'Serving Size': 4, 'Litres': 64, 'Category': 'produce',
                         'Information': 'Orange trees rely heavily on rain (green water), can require some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Okra': {'Formatted': 'okra', 'Serving Size': 4, 'Litres': 64, 'Category': 'produce',
                      'Information': 'Okra plants are heat and drought-tolerant so they are primarily rainfed (green water) but they are not profitably productive without supplemental irrigation (blue water), and they can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Green Beans': {'Formatted': 'greenbeans', 'Serving Size': 4, 'Litres': 61, 'Category': 'produce',
                             'Information': 'String beans plants are rainfed (green water), receive a significant amount of supplemental irrigation (blue water) because they are shallow-rooted and they can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'String beans': {'Formatted': 'stringbeans', 'Serving Size': 4, 'Litres': 61, 'Category': 'produce',
                              'Information': 'String beans plants are rainfed (green water), receive a significant amount of supplemental irrigation (blue water) because they are shallow-rooted and they can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Grapefruit': {'Formatted': 'grapefruit', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce',
                            'Information': 'Grapefruit trees are primarily rainfed (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Kiwifruit': {'Formatted': 'kiwifruit', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce',
                           'Information': 'Kiwi fruit vines need a warm climate and are primarily rainfed (green water), receive substantial irrigation in drier summer months (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water)'},
             'Papaya': {'Formatted': 'papaya', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce',
                        'Information': 'Papaya trees are primarily rainfed (green water) and can receive some supplemental irrigation (blue water).'},
             'Blackberries': {'Formatted': 'blackberries', 'Serving Size': 4, 'Litres': 45, 'Category': 'produce',
                              'Information': 'Blackberry bushes are grown in temperate areas and are largely rainfed (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Raspberries': {'Formatted': 'raspberries', 'Serving Size': 4, 'Litres': 45, 'Category': 'produce',
                             'Information': 'Raspberry bushes, which are related to blackberries and other brambles, grow in temperate areas and are largely rainfed (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Sweet potatoes': {'Formatted': 'sweetpotatoes', 'Serving Size': 4, 'Litres': 45, 'Category': 'produce',
                                'Information': 'Sweet potatoes are an indigenous root crop in the US and are primarily rainfed (green water), but in places where rainwater is inconsistent, they can receive a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Cucumbers': {'Formatted': 'cucumbers', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce',
                           'Information': 'Cucumber vines are grown in both fields and greenhouses. While cucumber vines grown in fields are rainfed (green water), all cucumber vines require supplemental irrigation (blue water) and they can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Eggplants': {'Formatted': 'eggplants', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce',
                           'Information': 'Eggplant plants are rainfed (green water) but are not drought-tolerant, so, they require supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Chili Peppers': {'Formatted': 'chilipeppers', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce',
                               'Information': 'Pepper bushes are a hot season crop and are primarily rainfed (green water), but are more productive with supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water). In the US, peppers are mostly drip irrigated, which increases the blue water footprint.'},
             'Sweet Peppers': {'Formatted': 'sweetpeppers', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce',
                               'Information': 'Pepper bushes are a hot season crop and are primarily rainfed (green water), but are more productive with supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water). In the US, peppers are mostly drip irrigated, which increases the blue water footprint.'},
             'Strawberries': {'Formatted': 'strawberries', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce',
                              'Information': 'Strawberry plants are rainfed (green water), they receive a significant amount of irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Pumpkins': {'Formatted': 'pumpkins', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce',
                          'Information': 'Pumpkin vines are primarily rainfed (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Squash': {'Formatted': 'squash', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce',
                        'Information': 'Squash vines are rainfed (green water), can receive supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Broccoli': {'Formatted': 'broccoli', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce',
                          'Information': 'Broccoli plants are primarily rainfed (green water), can require supplemental irrigation (blue water) because they are shallow-rooted and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Brussels sprouts': {'Formatted': 'brusselssprouts', 'Serving Size': 4, 'Litres': 34,
                                  'Category': 'produce',
                                  'Information': 'Brussels sprouts plants are rainfed (green water), can require irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Cauliflower': {'Formatted': 'cauliflower', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce',
                             'Information': 'Cauliflower plants are rainfed (green water), require supplemental irrigation (blue water) because they are shallow-rooted and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Potatoes': {'Formatted': 'potatoes', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce',
                          'Information': 'Potatoes are a root crop that are primarily rainfed (green water), require a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Spinach': {'Formatted': 'spinach', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce',
                         'Information': 'Spinach plants are primarily rainfed (green water), can receive irrigation water (blue water) especially in the US, and can cause a lot of water pollution (grey water) due to heavy use of fertilizer and herbicides use for weed control.'},
             'Cranberries': {'Formatted': 'cranberries', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce',
                             'Information': 'Cranberry bushes are grown in bogs or wetlands, are primarily rainfed (green water), receive substantial irrigation (blue water) through harvest flooding, and can cause water pollution from the significant application of fertilizer and/or pesticides (grey water).'},
             'Pineapples': {'Formatted': 'pineapples', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce',
                            'Information': 'Pineapples plants are almost entirely rainfed (green water) with minimal amounts of irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Cabbage': {'Formatted': 'cabbage', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce',
                         'Information': 'Cabbage plants (like other brassicas) are primarily rainfed (green water), are somewhat drought-tolerant yet can receive supplemental irrigation (blue water) to improve yield and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Kale': {'Formatted': 'kale', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce',
                      'Information': 'Kale plants are primarily rainfed (green water), can receive a significant amount of supplemental irrigation (blue water) because they are shallow-rooted and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Kohlrabi': {'Formatted': 'kohlrabi', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce',
                          'Information': 'Kohlrabi plants are primarily rainfed (green water), can receive significant supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Onions': {'Formatted': 'onions', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce',
                        'Information': 'Onion bulb plants are rainfed (green water), can require a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Melons': {'Formatted': 'melons', 'Serving Size': 4, 'Litres': 26, 'Category': 'produce',
                        'Information': 'Melon plants are mainly rainfed (green water), can receive some supplemental irrigation (blue water) and can cause water pollution from the application of fertilizer and/or pesticides (grey water).'},
             'Lettuce': {'Formatted': 'lettuce', 'Serving Size': 4, 'Litres': 26, 'Category': 'produce',
                         'Information': 'Lettuce plants are rainfed (green water), require a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Tea': {'Formatted': 'tea', 'Serving Size': 8, 'Litres': 26, 'Category': 'other',
                     'Information': 'Tea plants are primarily rainfed (green water), can receive a significant amount of supplemental irrigation (blue water) and can cause pollution from the use of fertilizer and/or pesticides (grey water). The grey water footprint is primarily associated with processing, packaging and transporting tea.'},
             'Carrots': {'Formatted': 'carrots', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce',
                         'Information': 'Carrots are a root crop that are primarily rainfed (green water), require supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Celery': {'Formatted': 'celery', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce',
                        'Information': 'Celery plants are rainfed (green water), require a significant amount of supplemental irrigation (blue water) because they are shallow-rooted and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Tomatoes': {'Formatted': 'tomatoes', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce',
                          'Information': 'Tomatoes are produced in both fields and greenhouses which has increased the irrigation requirements. Tomato plants are rainfed (green water) and irrigated (blue water) in about equal amounts and they can cause water pollution from the use of fertilizer and/or pesticides (grey water).'},
             'Turnips': {'Formatted': 'turnips', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce',
                         'Information': 'Turnips are cool season root vegetables that are rainfed (green water), can receive a significant amount of supplemental irrigation (blue water) and can cause water pollution from the use of fertilizer and/or pesticides (grey water).'}}
tip_dict = {'all': {
    'Tip1': 'Waste less:\n -  Because it takes a lot of water to get food to people’s plates, wasted food also means wasted water.\n -  The easiest and perhaps most effective thing to do is to plan out meals before heading to the store.',
    'Tip2': 'Choose Local Food:\n - Supporting local food production can help preserve water resources by keeping water usage for growing food within the local area. This reduces the need for transporting water across long distances.'},
    'meat': {
        'Tip1': 'Choose Better Meat: Choose pasture raised meat as much as possible as despite negligible differences between water footprints, their impact on water resources are different:\n - Pasture-fed (Green Water Footprint): Uses forage as feed grown from rainwater and manure is used as fertilisers.\n - Conventional (Blue Water Footprint): Uses feed like corn that need irrigation and animal waste is turned into manure lagoons that can pollute surrounding waters.',
        'Tip2': 'Eat Less Meat: On average, the water footprint of a vegan or vegetarian is around half that of a meat eater. Eating less meat and replacing it with less water-intensive plant-based alternatives can reduce water footprints'},
    'produce': {
        'Tip1': "Choose Organic:\n - Organic farms usually don't use pesticides or synthetic fertilisers which could run off of farm fields and pollute nearby waters. \n - Soils at organic farms tend to be much better at retaining nutrients and moisture, which reduces the risk of groundwater pollution.\n - Buying products grown organically helps support farms that are making big efforts to reduce water pollution, which means those products have a smaller gray water footprint.",
        'Tip2': ''}, 'processed foods': {
        'Tip1': 'In addition to growing the ingredients, processed foods require water for things like cleaning the food and machinery, pre-cooking the food, producing fuel for delivery and making packaging materials. Cutting back and replacing packaged foods with locally grown, organic alternatives can make a significant impact on your water footprint.',
        'Tip2': ''}, 'dried fruits': {
        'Tip1': 'Dried fruits have bigger water footprints than fresh because of water consumption associated with processing. To reduce their water footprint, individuals can opt for fresh produce over processed alternatives',
        'Tip2': ''}, 'dairy': {
        'Tip1': 'Reducing dairy consumption can help reduce the water footprint due to the significant water-intensive processes involved in producing feed grains for dairy cows and the potential water pollution caused by dairy farms ultimately leading to lower water consumption and environmental impact.',
        'Tip2': ''}, 'milled flour': {
        'Tip1': 'Reducing the consumption of milled flours and opting for whole grains like corn can contribute to lowering the water footprint, as processing milled flours requires additional water, while whole grains retain more of their natural water content, leading to more water-efficient food choices.',
        'Tip2': ''}}


# MAIN SCRIPT

def welcome_message():
    """
    Display a welcome message and introduce the water footprint calculator.
    """
    print("Welcome to the water footprint calculator!")
    print("This program is designed to give you an idea of how much water it takes to produce the foods you consume.")
    input("Press Enter to continue...")


# Function to display the list of food items
def display_food_items(food_object):
    """
    Display the list of available food items.

    Parameters:
        food_object (Food): The Food object initialized containing the list of food items.
    """
    print("Here are the list of food items: ")
    return food_object.display_available_foods()


def display_user_foods(food_object):
    """
        Display the list of food items added by the user along with their water footprints.

        Parameters:
            food_object (Food): The Food object containing the user-added food items.
        """
    i = 1
    for food, wf in food_object.user_foods.items():
        print(f"{i}. {food} ({wf} {food_object.unit})")
        i += 1


# Function to get user input for food consumption
def get_user_food_input(food_object):
    """
    Get user input for food consumption and calculate water footprint.

    Parameters:
        food_object (Food): The Food object to store user input and calculate water footprint.
    """
    while True:
        user_input = input("""\nWhich foods from the list above do you consume? Type in the name or the serial number. 
        If you want to see the list again, type 'list'. 
        If you want to see all the items you have added, type 'my list'. 
        If you have finished entering foods, type 'end'. 
        Type here: """)

        food = format_data(user_input, True)
        if food == "list":
            print(display_food_items(food_object))
        elif food == "mylist":
            display_user_foods(current_food_object)
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
                print(f"INFO: {food_object.print_info(food_object.find_food_item(food))}")
                print("\n")


# Function to get user input for receiving tips
def get_tips(tips_object):
    """
        Get user input to display tips for improving water footprint.

        Parameters:
            tips_object (Tips): The Tips object to retrieve and display tips.
        """
    tips_object.display_tips(item_key="Foods", message_before_items="\nSince you have chosen:",
                             general_category="all",
                             general_message="\nHere are some general tips to keep in mind: ")


def print_tips(tips_object):
    """
        Print tips to the user based on their input.

        Parameters:
            tips_object (Tips): The Tips object containing the user improvements and tips.
        """
    while True:
        want_tips = input(
            "\nWould you like some tips to improve your water footprint through better food habits? Type yes or no: ")
        if want_tips.lower() == "yes":
            get_tips(tips_object)
            input("\nThank you for using this water footprint calculator! Press enter to exit: ")
            return
        elif want_tips.lower() == "no":
            input("\nThank you for using this water footprint calculator! Press enter to exit: ")
            return
        else:
            print("That is not a valid input")


# Run the water footprint calculator
welcome_message()

# Initialize the Food object with the provided data
current_food_object = Food('week')
current_food_object.food_dict = food_dict
current_food_object.unit = "Litres"
current_food_object.serving = "Serving Size"
current_food_object.category = "Category"
current_food_object.info = "Information"

# Display available food items to the user
display_food_items(current_food_object)

# Get user input for food consumption
get_user_food_input(current_food_object)

# Calculate and print the total water footprint for the user
print(current_food_object.calculate_food_wf())

# Initialize the Tips object with the provided data
current_tips_object = Tips(all_items_dict=current_food_object.food_dict,
                           selected_items=list(current_food_object.user_foods.keys()))
current_tips_object.category_tips_dict = tip_dict
current_tips_object.category_column = "Category"

# Print tips for the user to improve their water footprint
print_tips(current_tips_object)
