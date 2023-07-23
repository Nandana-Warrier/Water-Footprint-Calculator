from water import *

current_user = Water('week')
foods = current_user.food_dict = current_user.import_food_csv("Water Footprint of Food Guide.csv", "Food", "Litres",
                                                              serving="Serving Size", category="Category")

end = False

while not end:
    user_input = input("""Which all food from this list do you consume? Type in the name or the serial number. 
    If you want the list, type 'list'. 
    If you want to see all the items you have added, type 'my list'. 
    If the list of food you consume has ended, type 'end'. 
    Type here: """)
    food = format_data(user_input, True)
    if food == "list":
        current_user.print_foods()
    elif food == "mylist":
        print(current_user.user_foods)
    elif food == "end":
        end = True
    else:
        items = current_user.check_food_item(user_input)
        if isinstance(items, dict):
            times = int(input(f"How many times do you have {items['food']} per week, assuming the serving size is {items['Serving Size']} ounces?: "))
            current_user.add_food_item(items['food'], items['wf'], times)

    print("\n")

print(current_user.calculate_food_wf())

want_tips = input("Would you like some tips to improve your water footprint through better food habits? Type yes or "
                  "no: ")
if want_tips == "yes":
    with open("Tips for Categories.csv") as file:
        current_user.display_tips(file, "Category", "Tip1", "Tip2")

input("Press input to exit: ")