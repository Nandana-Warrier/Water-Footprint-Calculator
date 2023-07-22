from water import *

current_user = Water(3000)
foods = current_user.food_dict = current_user.import_from_csv("Water Footprint of Food Guide.csv", "Food", "Litres",
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
        current_user.add_food_item(user_input)
    print("\n")

print(current_user.user_foods)
print(current_user.user_wfs)
print(current_user.calculate_food_wf())