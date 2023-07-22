from water import format_data
import csv

data_list = ["Formatted", self.unit, "Serving", "Category", "Explanation", "Other"]
the_list = [{'Food': 'Chocolate', 'Serving Size': '4', 'Gallons': '516', 'Litres': '1953', 'Category': 'other'},
            {'Food': 'Almonds', 'Serving Size': '4', 'Gallons': '483', 'Litres': '1828', 'Category': 'other'},
            {'Food': 'Beef', 'Serving Size': '4', 'Gallons': '463', 'Litres': '1753', 'Category': 'meat'},
            {'Food': 'Cashews', 'Serving Size': '4', 'Gallons': '427', 'Litres': '1616', 'Category': 'other'},
            {'Food': 'Pistachios', 'Serving Size': '4', 'Gallons': '341', 'Litres': '1291', 'Category': 'other'},
            {'Food': 'Hazelnuts', 'Serving Size': '4', 'Gallons': '316', 'Litres': '1196', 'Category': 'other'},
            {'Food': 'Lamb and mutton', 'Serving Size': '4', 'Gallons': '313', 'Litres': '1185', 'Category': 'meat'},
            {'Food': 'Walnuts', 'Serving Size': '4', 'Gallons': '279', 'Litres': '1056', 'Category': 'other'},
            {'Food': 'Dried Apples', 'Serving Size': '4', 'Gallons': '206', 'Litres': '780', 'Category': 'produce'},
            {'Food': 'Prunes', 'Serving Size': '4', 'Gallons': '187', 'Litres': '708', 'Category': 'produce'},
            {'Food': 'Pork and bacon', 'Serving Size': '4', 'Gallons': '180', 'Litres': '681', 'Category': 'meat'},
            {'Food': 'Butter', 'Serving Size': '4', 'Gallons': '167', 'Litres': '632', 'Category': 'processed foods'},
            {'Food': 'Goat', 'Serving Size': '4', 'Gallons': '166', 'Litres': '628', 'Category': 'meat'},
            {'Food': 'Quinoa', 'Serving Size': '4', 'Gallons': '135', 'Litres': '511', 'Category': 'other'},
            {'Food': 'Dried Apricots', 'Serving Size': '4', 'Gallons': '133', 'Litres': '503', 'Category': 'produce'},
            {'Food': 'Chicken', 'Serving Size': '4', 'Gallons': '130', 'Litres': '492', 'Category': 'meat'},
            {'Food': 'Turkey', 'Serving Size': '4', 'Gallons': '130', 'Litres': '492', 'Category': 'meat'},
            {'Food': 'Peanuts', 'Serving Size': '4', 'Gallons': '119', 'Litres': '450', 'Category': 'other'},
            {'Food': 'Soy burger', 'Serving Size': '4', 'Gallons': '113', 'Litres': '428',
             'Category': 'processed foods'},
            {'Food': 'Figs', 'Serving Size': '4', 'Gallons': '98', 'Litres': '371', 'Category': 'produce'},
            {'Food': 'Chicken Eggs', 'Serving Size': '4', 'Gallons': '98', 'Litres': '371', 'Category': 'other'},
            {'Food': 'Cows Milk', 'Serving Size': '4', 'Gallons': '98', 'Litres': '371', 'Category': 'processed foods'},
            {'Food': 'Cheese', 'Serving Size': '4', 'Gallons': '95', 'Litres': '360', 'Category': 'processed foods'},
            {'Food': 'Olives', 'Serving Size': '4', 'Gallons': '90', 'Litres': '341', 'Category': 'produce'},
            {'Food': 'Chestnuts', 'Serving Size': '4', 'Gallons': '83', 'Litres': '314', 'Category': 'other'},
            {'Food': 'Oatmeal', 'Serving Size': '4', 'Gallons': '76', 'Litres': '288', 'Category': 'processed foods'},
            {'Food': 'Tofu', 'Serving Size': '4', 'Gallons': '76', 'Litres': '288', 'Category': 'processed foods'},
            {'Food': 'Raisins', 'Serving Size': '4', 'Gallons': '73', 'Litres': '276', 'Category': 'produce'},
            {'Food': 'White Rice', 'Serving Size': '4', 'Gallons': '73', 'Litres': '276',
             'Category': 'processed foods'},
            {'Food': 'Apple juice', 'Serving Size': '8', 'Gallons': '71', 'Litres': '269',
             'Category': 'processed foods'},
            {'Food': 'Dates', 'Serving Size': '4', 'Gallons': '68', 'Litres': '257', 'Category': 'produce'},
            {'Food': 'Black-eyed peas', 'Serving Size': '4', 'Gallons': '67', 'Litres': '254', 'Category': 'produce'},
            {'Food': 'Cowpeas', 'Serving Size': '4', 'Gallons': '67', 'Litres': '254', 'Category': 'produce'},
            {'Food': 'Coffee', 'Serving Size': '8', 'Gallons': '66', 'Litres': '250', 'Category': 'processed foods'},
            {'Food': 'Plums', 'Serving Size': '4', 'Gallons': '65', 'Litres': '246', 'Category': 'produce'},
            {'Food': 'Asparagus', 'Serving Size': '4', 'Gallons': '65', 'Litres': '246', 'Category': 'produce'},
            {'Food': 'Brown Rice', 'Serving Size': '4', 'Gallons': '65', 'Litres': '246',
             'Category': 'processed foods'},
            {'Food': 'Soybeans', 'Serving Size': '4', 'Gallons': '64', 'Litres': '242', 'Category': 'produce'},
            {'Food': 'Edamame', 'Serving Size': '4', 'Gallons': '64', 'Litres': '242', 'Category': 'produce'},
            {'Food': 'Milk', 'Serving Size': '8', 'Gallons': '64', 'Litres': '242', 'Category': 'processed foods'},
            {'Food': 'Orange juice', 'Serving Size': '8', 'Gallons': '64', 'Litres': '242',
             'Category': 'processed foods'},
            {'Food': 'Lentils', 'Serving Size': '4', 'Gallons': '57', 'Litres': '216', 'Category': 'produce'},
            {'Food': 'Pasta', 'Serving Size': '4', 'Gallons': '56', 'Litres': '212', 'Category': 'processed foods'},
            {'Food': 'Wheat flour', 'Serving Size': '4', 'Gallons': '55', 'Litres': '208',
             'Category': 'processed foods'},
            {'Food': 'Guava', 'Serving Size': '4', 'Gallons': '54', 'Litres': '204', 'Category': 'produce'},
            {'Food': 'Mangoes', 'Serving Size': '4', 'Gallons': '54', 'Litres': '204', 'Category': 'produce'},
            {'Food': 'Pigeon peas', 'Serving Size': '4', 'Gallons': '54', 'Litres': '204', 'Category': 'produce'},
            {'Food': 'Pizza; sauce and cheese', 'Serving Size': '4', 'Gallons': '53', 'Litres': '201',
             'Category': 'processed foods'},
            {'Food': 'Dry Beans', 'Serving Size': '4', 'Gallons': '49', 'Litres': '185', 'Category': 'produce'},
            {'Food': 'Cherries', 'Serving Size': '4', 'Gallons': '48', 'Litres': '182', 'Category': 'produce'},
            {'Food': 'Plantains', 'Serving Size': '4', 'Gallons': '48', 'Litres': '182', 'Category': 'produce'},
            {'Food': 'Bread', 'Serving Size': '4', 'Gallons': '48', 'Litres': '182', 'Category': 'processed foods'},
            {'Food': 'Garbanzo beans', 'Serving Size': '4', 'Gallons': '41', 'Litres': '155', 'Category': 'produce'},
            {'Food': 'Chickpeas', 'Serving Size': '4', 'Gallons': '41', 'Litres': '155', 'Category': 'produce'},
            {'Food': 'Apricots', 'Serving Size': '4', 'Gallons': '39', 'Litres': '148', 'Category': 'produce'},
            {'Food': 'Corn flour', 'Serving Size': '4', 'Gallons': '38', 'Litres': '144',
             'Category': 'processed foods'},
            {'Food': 'Sweet Corn', 'Serving Size': '4', 'Gallons': '37', 'Litres': '140', 'Category': 'produce'},
            {'Food': 'Yogurt', 'Serving Size': '4', 'Gallons': '36', 'Litres': '136', 'Category': 'processed foods'},
            {'Food': 'Avocados', 'Serving Size': '4', 'Gallons': '35', 'Litres': '132', 'Category': 'produce'},
            {'Food': 'Wine', 'Serving Size': '5', 'Gallons': '35', 'Litres': '132', 'Category': 'other'},
            {'Food': 'Crisps', 'Serving Size': '4', 'Gallons': '31', 'Litres': '132', 'Category': 'processed foods'},
            {'Food': 'Potato chips', 'Serving Size': '4', 'Gallons': '31', 'Litres': '117',
             'Category': 'processed foods'},
            {'Food': 'Pears', 'Serving Size': '4', 'Gallons': '28', 'Litres': '106', 'Category': 'produce'},
            {'Food': 'Peaches and Nectarines', 'Serving Size': '4', 'Gallons': '27', 'Litres': '102',
             'Category': 'produce'},
            {'Food': 'Soft drink', 'Serving Size': '8', 'Gallons': '26', 'Litres': '98', 'Category': 'processed foods'},
            {'Food': 'Apples', 'Serving Size': '4', 'Gallons': '25', 'Litres': '95', 'Category': 'produce'},
            {'Food': 'Blueberries', 'Serving Size': '4', 'Gallons': '25', 'Litres': '95', 'Category': 'produce'},
            {'Food': 'Artichokes', 'Serving Size': '4', 'Gallons': '25', 'Litres': '95', 'Category': 'produce'},
            {'Food': 'Bananas', 'Serving Size': '4', 'Gallons': '24', 'Litres': '91', 'Category': 'produce'},
            {'Food': 'Tangerines', 'Serving Size': '4', 'Gallons': '22', 'Litres': '83', 'Category': 'produce'},
            {'Food': 'Clementines', 'Serving Size': '4', 'Gallons': '22', 'Litres': '83', 'Category': 'produce'},
            {'Food': 'Mandarins', 'Serving Size': '4', 'Gallons': '22', 'Litres': '83', 'Category': 'produce'},
            {'Food': 'Broad beans', 'Serving Size': '4', 'Gallons': '20', 'Litres': '76', 'Category': 'produce'},
            {'Food': 'Lemons', 'Serving Size': '4', 'Gallons': '19', 'Litres': '72', 'Category': 'produce'},
            {'Food': 'Limes', 'Serving Size': '4', 'Gallons': '19', 'Litres': '72', 'Category': 'produce'},
            {'Food': 'Beer', 'Serving Size': '8', 'Gallons': '19', 'Litres': '72', 'Category': 'other'},
            {'Food': 'Soy milk', 'Serving Size': '8', 'Gallons': '19', 'Litres': '72', 'Category': 'processed foods'},
            {'Food': 'Grapes', 'Serving Size': '4', 'Gallons': '18', 'Litres': '68', 'Category': 'produce'},
            {'Food': 'Garlic', 'Serving Size': '4', 'Gallons': '18', 'Litres': '68', 'Category': 'produce'},
            {'Food': 'Fresh Peas', 'Serving Size': '', 'Gallons': '18', 'Litres': '68', 'Category': 'produce'},
            {'Food': 'Taro', 'Serving Size': '4', 'Gallons': '18', 'Litres': '68', 'Category': 'produce'},
            {'Food': 'Oranges', 'Serving Size': '4', 'Gallons': '17', 'Litres': '64', 'Category': 'produce'},
            {'Food': 'Okra', 'Serving Size': '4', 'Gallons': '17', 'Litres': '64', 'Category': 'produce'},
            {'Food': 'Green Beans', 'Serving Size': '4', 'Gallons': '16', 'Litres': '61', 'Category': 'produce'},
            {'Food': 'String beans', 'Serving Size': '4', 'Gallons': '16', 'Litres': '61', 'Category': 'produce'},
            {'Food': 'Grapefruit', 'Serving Size': '4', 'Gallons': '15', 'Litres': '57', 'Category': 'produce'},
            {'Food': 'Kiwifruit', 'Serving Size': '4', 'Gallons': '15', 'Litres': '57', 'Category': 'produce'},
            {'Food': 'Papaya', 'Serving Size': '4', 'Gallons': '15', 'Litres': '57', 'Category': 'produce'},
            {'Food': 'Blackberries', 'Serving Size': '4', 'Gallons': '12', 'Litres': '45', 'Category': 'produce'},
            {'Food': 'Raspberries', 'Serving Size': '4', 'Gallons': '12', 'Litres': '45', 'Category': 'produce'},
            {'Food': 'Sweet potatoes', 'Serving Size': '4', 'Gallons': '12', 'Litres': '45', 'Category': 'produce'},
            {'Food': 'Cucumbers', 'Serving Size': '4', 'Gallons': '11', 'Litres': '42', 'Category': 'produce'},
            {'Food': 'Eggplants', 'Serving Size': '4', 'Gallons': '11', 'Litres': '42', 'Category': 'produce'},
            {'Food': 'Chili Peppers', 'Serving Size': '4', 'Gallons': '11', 'Litres': '42', 'Category': 'produce'},
            {'Food': 'Sweet Peppers', 'Serving Size': '4', 'Gallons': '11', 'Litres': '42', 'Category': 'produce'},
            {'Food': 'Strawberries', 'Serving Size': '4', 'Gallons': '10', 'Litres': '38', 'Category': 'produce'},
            {'Food': 'Pumpkins', 'Serving Size': '4', 'Gallons': '10', 'Litres': '38', 'Category': 'produce'},
            {'Food': 'Squash', 'Serving Size': '4', 'Gallons': '10', 'Litres': '38', 'Category': 'produce'},
            {'Food': 'Broccoli', 'Serving Size': '4', 'Gallons': '9', 'Litres': '34', 'Category': 'produce'},
            {'Food': 'Brussels sprouts', 'Serving Size': '4', 'Gallons': '9', 'Litres': '34', 'Category': 'produce'},
            {'Food': 'Cauliflower', 'Serving Size': '4', 'Gallons': '9', 'Litres': '34', 'Category': 'produce'},
            {'Food': 'Potatoes', 'Serving Size': '4', 'Gallons': '9', 'Litres': '34', 'Category': 'produce'},
            {'Food': 'Spinach', 'Serving Size': '4', 'Gallons': '9', 'Litres': '34', 'Category': 'produce'},
            {'Food': 'Cranberries', 'Serving Size': '4', 'Gallons': '8', 'Litres': '30', 'Category': 'produce'},
            {'Food': 'Pineapples', 'Serving Size': '4', 'Gallons': '8', 'Litres': '30', 'Category': 'produce'},
            {'Food': 'Cabbage', 'Serving Size': '4', 'Gallons': '8', 'Litres': '30', 'Category': 'produce'},
            {'Food': 'Kale', 'Serving Size': '4', 'Gallons': '8', 'Litres': '30', 'Category': 'produce'},
            {'Food': 'Kohlrabi', 'Serving Size': '4', 'Gallons': '8', 'Litres': '30', 'Category': 'produce'},
            {'Food': 'Onions', 'Serving Size': '4', 'Gallons': '8', 'Litres': '30', 'Category': 'produce'},
            {'Food': 'Cantaloupe and other melons', 'Serving Size': '4', 'Gallons': '7', 'Litres': '26',
             'Category': 'produce'},
            {'Food': 'Watermelons', 'Serving Size': '4', 'Gallons': '7', 'Litres': '26', 'Category': 'produce'},
            {'Food': 'Lettuce', 'Serving Size': '4', 'Gallons': '7', 'Litres': '26', 'Category': 'produce'},
            {'Food': 'Tea', 'Serving Size': '8', 'Gallons': '7', 'Litres': '26', 'Category': 'other'},
            {'Food': 'Carrots', 'Serving Size': '4', 'Gallons': '6', 'Litres': '23', 'Category': 'produce'},
            {'Food': 'Celery', 'Serving Size': '4', 'Gallons': '6', 'Litres': '23', 'Category': 'produce'},
            {'Food': 'Tomatoes', 'Serving Size': '4', 'Gallons': '6', 'Litres': '23', 'Category': 'produce'},
            {'Food': 'Turnips', 'Serving Size': '4', 'Gallons': '6', 'Litres': '23', 'Category': 'produce'}]
keys = ["Tip1", "Tip2", "Tip3", "Tip4", "Tip5"]


def og_create_value_dict():
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


def create_value_dict(pros_keys, og_keys, replace_spaces):
    """Returns list of dictionaries with characteristics for each key in the keys list from data_list"""
    value_list = []
    for key, value in zip(pros_keys, og_keys):
        a_dict = {}
        a_dict.update({key: format_data(value, replace_spaces)} if key is not None else {})
        value_list.append(a_dict)
    return value_list


