from food import *
from tips import *

test_food_obj = Food('week')
test_food_tips_obj = Tips(all_items=test_food_obj.food_dict, user_items=test_food_obj.user_foods)
foods = test_food_obj.food_dict = test_food_obj.use_food_csv("Water Footprint of Food Guide.csv", "Food", "Litres",
                                                             serving="Serving Size", category="Category")
test_food_tips_obj.import_tips("Tips for Categories.csv", "Category", "Tip1", "Tip2")

print(test_food_obj.food_dict)
print(test_food_tips_obj.category_tips)

# noinspection SpellCheckingInspection
food_dict = {'Chocolate': {'Formatted': 'chocolate', 'Serving Size': 4, 'Litres': 1953, 'Category': 'other'},
             'Almonds': {'Formatted': 'almonds', 'Serving Size': 4, 'Litres': 1828, 'Category': 'other'},
             'Beef': {'Formatted': 'beef', 'Serving Size': 4, 'Litres': 1753, 'Category': 'meat'},
             'Cashews': {'Formatted': 'cashews', 'Serving Size': 4, 'Litres': 1616, 'Category': 'other'},
             'Pistachios': {'Formatted': 'pistachios', 'Serving Size': 4, 'Litres': 1291, 'Category': 'other'},
             'Hazelnuts': {'Formatted': 'hazelnuts', 'Serving Size': 4, 'Litres': 1196, 'Category': 'other'},
             'Lamb and mutton': {'Formatted': 'lambandmutton', 'Serving Size': 4, 'Litres': 1185, 'Category': 'meat'},
             'Walnuts': {'Formatted': 'walnuts', 'Serving Size': 4, 'Litres': 1056, 'Category': 'other'},
             'Dried Apples': {'Formatted': 'driedapples', 'Serving Size': 4, 'Litres': 780, 'Category': 'produce'},
             'Prunes': {'Formatted': 'prunes', 'Serving Size': 4, 'Litres': 708, 'Category': 'produce'},
             'Pork and bacon': {'Formatted': 'porkandbacon', 'Serving Size': 4, 'Litres': 681, 'Category': 'meat'},
             'Butter': {'Formatted': 'butter', 'Serving Size': 4, 'Litres': 632, 'Category': 'processedfoods'},
             'Goat': {'Formatted': 'goat', 'Serving Size': 4, 'Litres': 628, 'Category': 'meat'},
             'Quinoa': {'Formatted': 'quinoa', 'Serving Size': 4, 'Litres': 511, 'Category': 'other'},
             'Dried Apricots': {'Formatted': 'driedapricots', 'Serving Size': 4, 'Litres': 503, 'Category': 'produce'},
             'Chicken': {'Formatted': 'chicken', 'Serving Size': 4, 'Litres': 492, 'Category': 'meat'},
             'Turkey': {'Formatted': 'turkey', 'Serving Size': 4, 'Litres': 492, 'Category': 'meat'},
             'Peanuts': {'Formatted': 'peanuts', 'Serving Size': 4, 'Litres': 450, 'Category': 'other'},
             'Soy burger': {'Formatted': 'soyburger', 'Serving Size': 4, 'Litres': 428, 'Category': 'processedfoods'},
             'Figs': {'Formatted': 'figs', 'Serving Size': 4, 'Litres': 371, 'Category': 'produce'},
             'Chicken Eggs': {'Formatted': 'chickeneggs', 'Serving Size': 4, 'Litres': 371, 'Category': 'other'},
             'Cows Milk': {'Formatted': 'cowsmilk', 'Serving Size': 4, 'Litres': 371, 'Category': 'processedfoods'},
             'Cheese': {'Formatted': 'cheese', 'Serving Size': 4, 'Litres': 360, 'Category': 'processedfoods'},
             'Olives': {'Formatted': 'olives', 'Serving Size': 4, 'Litres': 341, 'Category': 'produce'},
             'Chestnuts': {'Formatted': 'chestnuts', 'Serving Size': 4, 'Litres': 314, 'Category': 'other'},
             'Oatmeal': {'Formatted': 'oatmeal', 'Serving Size': 4, 'Litres': 288, 'Category': 'processedfoods'},
             'Tofu': {'Formatted': 'tofu', 'Serving Size': 4, 'Litres': 288, 'Category': 'processedfoods'},
             'Raisins': {'Formatted': 'raisins', 'Serving Size': 4, 'Litres': 276, 'Category': 'produce'},
             'White Rice': {'Formatted': 'whiterice', 'Serving Size': 4, 'Litres': 276, 'Category': 'processedfoods'},
             'Apple juice': {'Formatted': 'applejuice', 'Serving Size': 8, 'Litres': 269, 'Category': 'processedfoods'},
             'Dates': {'Formatted': 'dates', 'Serving Size': 4, 'Litres': 257, 'Category': 'produce'},
             'Black-eyed peas': {'Formatted': 'black-eyedpeas', 'Serving Size': 4, 'Litres': 254,
                                 'Category': 'produce'},
             'Cowpeas': {'Formatted': 'cowpeas', 'Serving Size': 4, 'Litres': 254, 'Category': 'produce'},
             'Coffee': {'Formatted': 'coffee', 'Serving Size': 8, 'Litres': 250, 'Category': 'processedfoods'},
             'Plums': {'Formatted': 'plums', 'Serving Size': 4, 'Litres': 246, 'Category': 'produce'},
             'Asparagus': {'Formatted': 'asparagus', 'Serving Size': 4, 'Litres': 246, 'Category': 'produce'},
             'Brown Rice': {'Formatted': 'brownrice', 'Serving Size': 4, 'Litres': 246, 'Category': 'processedfoods'},
             'Soybeans': {'Formatted': 'soybeans', 'Serving Size': 4, 'Litres': 242, 'Category': 'produce'},
             'Edamame': {'Formatted': 'edamame', 'Serving Size': 4, 'Litres': 242, 'Category': 'produce'},
             'Milk': {'Formatted': 'milk', 'Serving Size': 8, 'Litres': 242, 'Category': 'processedfoods'},
             'Orange juice': {'Formatted': 'orangejuice', 'Serving Size': 8, 'Litres': 242,
                              'Category': 'processedfoods'},
             'Lentils': {'Formatted': 'lentils', 'Serving Size': 4, 'Litres': 216, 'Category': 'produce'},
             'Pasta': {'Formatted': 'pasta', 'Serving Size': 4, 'Litres': 212, 'Category': 'processedfoods'},
             'Wheat flour': {'Formatted': 'wheatflour', 'Serving Size': 4, 'Litres': 208, 'Category': 'processedfoods'},
             'Guava': {'Formatted': 'guava', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce'},
             'Mangoes': {'Formatted': 'mangoes', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce'},
             'Pigeon peas': {'Formatted': 'pigeonpeas', 'Serving Size': 4, 'Litres': 204, 'Category': 'produce'},
             'Pizza; sauce and cheese': {'Formatted': 'pizza;sauceandcheese', 'Serving Size': 4, 'Litres': 201,
                                         'Category': 'processedfoods'},
             'Dry Beans': {'Formatted': 'drybeans', 'Serving Size': 4, 'Litres': 185, 'Category': 'produce'},
             'Cherries': {'Formatted': 'cherries', 'Serving Size': 4, 'Litres': 182, 'Category': 'produce'},
             'Plantains': {'Formatted': 'plantains', 'Serving Size': 4, 'Litres': 182, 'Category': 'produce'},
             'Bread': {'Formatted': 'bread', 'Serving Size': 4, 'Litres': 182, 'Category': 'processedfoods'},
             'Garbanzo beans': {'Formatted': 'garbanzobeans', 'Serving Size': 4, 'Litres': 155, 'Category': 'produce'},
             'Chickpeas': {'Formatted': 'chickpeas', 'Serving Size': 4, 'Litres': 155, 'Category': 'produce'},
             'Apricots': {'Formatted': 'apricots', 'Serving Size': 4, 'Litres': 148, 'Category': 'produce'},
             'Corn flour': {'Formatted': 'cornflour', 'Serving Size': 4, 'Litres': 144, 'Category': 'processedfoods'},
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
             'Soft drink': {'Formatted': 'softdrink', 'Serving Size': 8, 'Litres': 98, 'Category': 'processedfoods'},
             'Apples': {'Formatted': 'apples', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce'},
             'Blueberries': {'Formatted': 'blueberries', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce'},
             'Artichokes': {'Formatted': 'artichokes', 'Serving Size': 4, 'Litres': 95, 'Category': 'produce'},
             'Bananas': {'Formatted': 'bananas', 'Serving Size': 4, 'Litres': 91, 'Category': 'produce'},
             'Tangerines': {'Formatted': 'tangerines', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce'},
             'Clementines': {'Formatted': 'clementines', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce'},
             'Mandarins': {'Formatted': 'mandarins', 'Serving Size': 4, 'Litres': 83, 'Category': 'produce'},
             'Broad beans': {'Formatted': 'broadbeans', 'Serving Size': 4, 'Litres': 76, 'Category': 'produce'},
             'Lemons': {'Formatted': 'lemons', 'Serving Size': 4, 'Litres': 72, 'Category': 'produce'},
             'Limes': {'Formatted': 'limes', 'Serving Size': 4, 'Litres': 72, 'Category': 'produce'},
             'Beer': {'Formatted': 'beer', 'Serving Size': 8, 'Litres': 72, 'Category': 'other'},
             'Soy milk': {'Formatted': 'soymilk', 'Serving Size': 8, 'Litres': 72, 'Category': 'processedfoods'},
             'Grapes': {'Formatted': 'grapes', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce'},
             'Garlic': {'Formatted': 'garlic', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce'},
             'Fresh Peas': {'Formatted': 'freshpeas', 'Serving Size': '', 'Litres': 68, 'Category': 'produce'},
             'Taro': {'Formatted': 'taro', 'Serving Size': 4, 'Litres': 68, 'Category': 'produce'},
             'Oranges': {'Formatted': 'oranges', 'Serving Size': 4, 'Litres': 64, 'Category': 'produce'},
             'Okra': {'Formatted': 'okra', 'Serving Size': 4, 'Litres': 64, 'Category': 'produce'},
             'Green Beans': {'Formatted': 'greenbeans', 'Serving Size': 4, 'Litres': 61, 'Category': 'produce'},
             'String beans': {'Formatted': 'stringbeans', 'Serving Size': 4, 'Litres': 61, 'Category': 'produce'},
             'Grapefruit': {'Formatted': 'grapefruit', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce'},
             'Kiwifruit': {'Formatted': 'kiwifruit', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce'},
             'Papaya': {'Formatted': 'papaya', 'Serving Size': 4, 'Litres': 57, 'Category': 'produce'},
             'Blackberries': {'Formatted': 'blackberries', 'Serving Size': 4, 'Litres': 45, 'Category': 'produce'},
             'Raspberries': {'Formatted': 'raspberries', 'Serving Size': 4, 'Litres': 45, 'Category': 'produce'},
             'Sweet potatoes': {'Formatted': 'sweetpotatoes', 'Serving Size': 4, 'Litres': 45, 'Category': 'produce'},
             'Cucumbers': {'Formatted': 'cucumbers', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce'},
             'Eggplants': {'Formatted': 'eggplants', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce'},
             'Chili Peppers': {'Formatted': 'chilipeppers', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce'},
             'Sweet Peppers': {'Formatted': 'sweetpeppers', 'Serving Size': 4, 'Litres': 42, 'Category': 'produce'},
             'Strawberries': {'Formatted': 'strawberries', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce'},
             'Pumpkins': {'Formatted': 'pumpkins', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce'},
             'Squash': {'Formatted': 'squash', 'Serving Size': 4, 'Litres': 38, 'Category': 'produce'},
             'Broccoli': {'Formatted': 'broccoli', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce'},
             'Brussels sprouts': {'Formatted': 'brusselssprouts', 'Serving Size': 4, 'Litres': 34,
                                  'Category': 'produce'},
             'Cauliflower': {'Formatted': 'cauliflower', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce'},
             'Potatoes': {'Formatted': 'potatoes', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce'},
             'Spinach': {'Formatted': 'spinach', 'Serving Size': 4, 'Litres': 34, 'Category': 'produce'},
             'Cranberries': {'Formatted': 'cranberries', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
             'Pineapples': {'Formatted': 'pineapples', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
             'Cabbage': {'Formatted': 'cabbage', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
             'Kale': {'Formatted': 'kale', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
             'Kohlrabi': {'Formatted': 'kohlrabi', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
             'Onions': {'Formatted': 'onions', 'Serving Size': 4, 'Litres': 30, 'Category': 'produce'},
             'Cantaloupe and other melons': {'Formatted': 'cantaloupeandothermelons', 'Serving Size': 4, 'Litres': 26,
                                             'Category': 'produce'},
             'Watermelons': {'Formatted': 'watermelons', 'Serving Size': 4, 'Litres': 26, 'Category': 'produce'},
             'Lettuce': {'Formatted': 'lettuce', 'Serving Size': 4, 'Litres': 26, 'Category': 'produce'},
             'Tea': {'Formatted': 'tea', 'Serving Size': 8, 'Litres': 26, 'Category': 'other'},
             'Carrots': {'Formatted': 'carrots', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'},
             'Celery': {'Formatted': 'celery', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'},
             'Tomatoes': {'Formatted': 'tomatoes', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'},
             'Turnips': {'Formatted': 'turnips', 'Serving Size': 4, 'Litres': 23, 'Category': 'produce'}}
tip_dict = {'meat': {'Tip1': 'Choose Better Meat: Choose pasture raised meat as much as possible as despite '
                             'negligible differences between water footprints, their impact on water resources are '
                             'different:\n - Pasture-fed (Green Water Footprint): Uses forage as feed grown from '
                             'rainwater and manure is used as fertilisers.\n - Conventional (Blue Water Footprint): '
                             'Uses feed like corn that need irrigation and animal waste is turned into manure lagoons '
                             'that can pollute surrounding waters.', 'Tip2': 'Eat Less Meat: On average, '
                                                                             'the water footprint of a vegan or '
                                                                             'vegetarian is around half that of a '
                                                                             'meat eater. Eating less meat and '
                                                                             'replacing it with less water-intensive '
                                                                             'plant-based alternatives can reduce '
                                                                             'water footprints'}, 'produce': {
    'Tip1': "Choose Organic:\n - Organic farms usually don't use pesticides or synthetic fertilisers which could run "
            "off of farm fields and pollute nearby waters. \n - Soils at organic farms tend to be much better at "
            "retaining nutrients and moisture, which reduces the risk of groundwater pollution.\n - Buying products "
            "grown organically helps support farms that are making big efforts to reduce water pollution, which means "
            "those products have a smaller gray water footprint.",
    'Tip2': ''}, 'processed foods': {
    'Tip1': 'In addition to growing the ingredients, processed foods require water for things like cleaning the food '
            'and machinery, pre-cooking the food, producing fuel for delivery and making packaging materials. Cutting '
            'back and replacing packaged foods with locally grown, organic alternatives can make a significant impact '
            'on your water footprint.',
    'Tip2': ''}}
