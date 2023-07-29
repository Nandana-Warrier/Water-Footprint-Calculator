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
