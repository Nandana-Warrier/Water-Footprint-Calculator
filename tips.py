from water_library import *


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
        value_dicts = create_value_dict([tip1, tip2, tip3, tip4, tip5], tip_dicts, False)
        i = 0
        for _ in value_dicts:
            self.category_tips_dict[tip_dicts[i][category]] = value_dicts[i]
            i += 1
        return self.category_tips_dict

    def create_user_improvements(self, all_category=None):
        """
        Create user improvements based on the selected items.

        Parameters:
            all_category (str, optional): Title of the category where general tips are stored.
        """
        items = {}
        for item in self.selected_items:
            for tip_category in self.category_tips_dict:
                if self.all_items[item][self.category_column] == format_data(tip_category, True):
                    items[item] = self.category_tips_dict[tip_category]
        if all_category:
            items["all"] = self.category_tips_dict[all_category]

        self.user_improvements = combine_keys_with_same_values(items)

    def display_tips(self, message_before_tips=None, message_before_items=None, general_category=None,
                     general_message=None):
        """
        Display tips to the user.

        Parameters:
            message_before_tips (str, optional): The message to be displayed before printing tips of a category.
            message_before_items (str, optional): The message to be displayed before printing items of a category.
            general_category (str, optional): Title of the category where general tips are stored.
            general_message (str, optional): The message to be displayed before printing the general tips.
        """
        self.create_user_improvements(general_category)

        def print_tips(k, message=None):
            print(message) if isinstance(message, str) else print("\n")
            for tip in self.user_improvements[k]:
                the_tip = f" {self.user_improvements[k][tip]}"
                if the_tip != "" and the_tip != " ":
                    print(f"➢ {self.user_improvements[k][tip]}")

        if len(self.user_improvements) == 1:
            print_tips(general_category, general_message)
        else:
            if message_before_items:
                for key in self.user_improvements:
                    if key == general_category:
                        message_before_tips = general_message
                    else:
                        print(message_before_items)
                        if isinstance(key, tuple):
                            for element in key:
                                print(f"• {element}")
                        else:
                            print(f"• {key}")
                    print_tips(key, message_before_tips)
            else:
                print(message_before_items)
                for key in self.user_improvements:
                    print_tips(key)

    # TODO: Add more categories and tips. Improve user interface in general

