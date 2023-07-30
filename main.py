from food import *
from tips import *


def welcome_message():
    print("Welcome to the water footprint calculator!")
    print("This program is designed to give you an idea of how much water it takes to produce the foods you consume.")
    input("Press Enter to continue...")
    return None


# Function to get food data from CSV and create Food and Tips objects
def get_food_data():
    food_object = Food('week')
    foods_dict = food_object.load_food_csv("Water Footprint of Food Guide.csv", "Food", "Litres",
                                           serving="Serving Size", category="Category", info="Information")
    return food_object, foods_dict


# Function to display the list of food items
def display_food_items(food_object):
    print("Here are the list of food items: ")
    return food_object.display_available_foods()


def display_user_foods(food_object):
    i = 1
    for food, wf in food_object.user_foods.items():
        print(f"{i}. {food} ({wf} {food_object.unit})")
        i += 1


# Function to get user input for food consumption
def get_user_food_input(food_object):
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
def get_tips():
    current_tips_object = Tips(all_items_dict=current_food_object.food_dict,
                               selected_items=list(current_food_object.user_foods.keys()))
    current_tips_object.import_tips("Tips for Categories.csv", "Category", "Tip1", "Tip2")
    current_tips_object.display_tips(item_key="Foods", message_before_items="\nSince you have chosen:",
                                     general_category="all",
                                     general_message="\nHere are some general tips to keep in mind: ")


def print_tips():
    while True:
        want_tips = input(
            "\nWould you like some tips to improve your water footprint through better food habits? Type yes or no: ")
        if want_tips.lower() == "yes":
            get_tips()
            input("\nThank you for using this water footprint calculator! Press enter to exit: ")
            return
        elif want_tips.lower() == "no":
            input("\nThank you for using this water footprint calculator! Press enter to exit: ")
            return
        else:
            print("That is not a valid input")


welcome_message()

current_food_object, foods = get_food_data()

display_food_items(current_food_object)

get_user_food_input(current_food_object)

print(current_food_object.calculate_food_wf())

print_tips()
