from food import *
from tips import *

input("Welcome to the water footprint calculator!")
input("This program is just to give you an idea of how much water it takes for making the foods you may have been "
      "taking without a second thought. ")

food_obj = Food('week')
food_tips_obj = Tips(all_items=food_obj.food_dict, user_items=food_obj.user_foods)
foods = food_obj.food_dict = food_obj.use_food_csv("Water Footprint of Food Guide.csv", "Food", "Litres",
                                                   serving="Serving Size", category="Category")

print("Here are the list of food items: ")
print(food_obj.print_foods())

end = False

while not end:
    user_input = input("""\nWhich all food from this list do you consume? Type in the name or the serial number. 
    If you want the list, type 'list'. 
    If you want to see all the items you have added, type 'my list'. 
    If the list of food you consume has ended, type 'end'. 
    Type here: """)
    food = format_data(user_input, True)
    if food == "list":
        food_obj.print_foods()
    elif food == "mylist":
        print(food_obj.user_foods)
    elif food == "end":
        end = True
    else:
        items = food_obj.check_food_item(user_input)
        if isinstance(items, dict):
            times = ""
            while not isinstance(times, float) and not isinstance(times, int):
                times = input(f"How many times do you have {items['food']} per week, assuming the serving "
                              f"size is {items['Serving Size']} ounces?: ")
                try:
                    times = float(times)
                except ValueError:
                    print(f"That is not a number. Please try again")
            food_obj.add_food_item(items['food'], items['wf'], times)

    print("\n")

print(food_obj.calculate_food_wf())

want_tips = input("Would you like some tips to improve your water footprint through better food habits? Type yes or "
                  "no: ")
if want_tips == "yes":
    food_tips_obj.import_tips("Tips for Categories.csv", "Category", "Tip1", "Tip2")
    food_tips_obj.display_tips("\nSince you have chosen:", "\nKeep in mind that:")
input("\nThank you for using this water footprint calculator! Press input to exit: ")
