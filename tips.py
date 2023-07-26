from water_library import *
import csv


class Tips:
    def __init__(self, all_items: dict, user_items: list):
        """
        Parameters:
            all_items (dict): Should contain the items as keys and dictionaries as values. Value dictionaries should
            have 'category' as key and value should correspond to a category that exists in the file with tips of each
            category.
            user_items (list): Should contain the list of all items that the user has selected in the
        """
        self.category_title = ""
        self.category_tips = {}  # To contain {category: {tip1: "", tip2: "" ..}..}
        self.all_items = all_items
        self.user_items = user_items  # This list has all the user-selected items on which tips are applicable
        self.user_improvements = {}  # This dictionary has all tips for the user to improve their water footprint

    # noinspection PyIncorrectDocstring
    def import_tips(self, file, category, tip1, tip2=None, tip3=None, tip4=None, tip5=None):
        """Parameters:
                category: The title under which categories are stored in your file
                tip1, tip2, tip3, tip4, tip5: The titles under which the tips are stored"""

        tip_dicts = []  # To contain [{category:"", "tip1: "..}, {category: "", "tip1": ..}..]
        self.category_title = category
        obj = import_csv(file)
        for row in obj:
            tip_dicts.append(row)
        value_dicts = create_value_dict([tip1, tip2, tip3, tip4, tip5], tip_dicts, False)
        i = 0
        for _ in value_dicts:
            self.category_tips[tip_dicts[i][category]] = value_dicts[i]
            i += 1

    def create_user_improvements(self):
        items = {}
        for item in self.user_items:
            for tip_category in self.category_tips:
                if self.all_items[item][self.category_title] == format_data(tip_category, True):
                    items[item] = self.category_tips[tip_category]

        self.user_improvements = combine_keys_with_same_values(items)

    def display_tips(self, message_before_foods, message_before_tips):
        self.create_user_improvements()
        # To check all the tips that apply to the user through self.user_items
        for key in self.user_improvements:
            print(message_before_foods)
            if isinstance(key, tuple):
                for element in key:
                    print(f"• {element}")
            else:
                print(f"• {key}")

            print(message_before_tips)

            for tip in self.user_improvements[key]:
                if tip is not None:
                    # To check if the_tip is not None
                    the_tip = f" {self.user_improvements[key][tip]}"
                    if the_tip != "" and the_tip != " ":
                        print(f"\n➢ {self.user_improvements[key][tip]}")

    # TODO: Add more categories and tips. Improve user interface in general
    # I am adding this comment and committing to see whether it appears in the master branch
