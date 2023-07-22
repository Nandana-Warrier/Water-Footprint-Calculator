from water import format_data
import csv


def import_from_csv(file, food, litres=None, gallons=None, serving=None, other=None):
    if not litres and not gallons:
        return "Please enter at least one unit"

    the_list = []

    def create_value_dict():
        value_list = []
        for dic in the_list:
            a_dict = {"Formatted": format_data(dic[food])}
            if litres is not None:
                a_dict["Litres"] = dic[litres]
            if gallons is not None:
                a_dict["Gallons"] = dic[gallons]
            if serving is not None:
                a_dict["Serving"] = dic[serving]
            if other is not None:
                a_dict["Other"] = dic[other]
            value_list.append(a_dict)
        return value_list

    def import_function():
        food_dict = {}
        in_list = create_value_dict()
        i = 0
        for d in the_list:
            value_dict = in_list[i]
            food_dict[the_list[i][food]] = value_dict
            i += 1
        return food_dict

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
        return import_function()


my_dict = import_from_csv("Trials.csv", "Food", "Litres", "Gallons", "Serving Size")
print(my_dict)
