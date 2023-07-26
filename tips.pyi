from food import *

class Tips:
    def display_tips(self, file, category, tip1, tip2=None, tip3=None, tip4=None, tip5=None):
        """Displays all applicable tips to improve the user's water footprints.
        IMPORTANT: argument for parameter (title of the csv file which has categories listed) should be same for all
        imported files"""
        tip_dicts = []  # To contain [{category:"", "tip1: "..}, {category: "", "tip1": ..}..]
        category_tips = {}  # To contain {category: {tip1: "", tip2: "" ..}..}
        obj = csv.DictReader(file)
        for row in obj:
            tip_dicts.append(row)
        value_dicts = create_value_dict([category, tip1, tip2, tip3, tip4, tip5], tip_dicts, False)
        i = 0
        for d in value_dicts:
            category_tips[tip_dicts[i][category]] = value_dicts[i]
            i += 1

        # To check all the tips that apply to the user through self.user_foods
        foods = {}
        for food in self.user_foods:
            for tip_category in category_tips:
                if self.food_dict[food][category] == format_data(tip_category, True):
                    foods[food] = category_tips[tip_category]

        self.user_improvements = combine_keys_with_same_values(foods)

        for key in self.user_improvements:
            print("\nSince you have added: ")
            if isinstance(key, tuple):
                for element in key:
                    print(f"• {element}")
            else:
                print(f"• {key}")

            for tip in [tip1, tip2, tip3, tip4, tip5]:
                if tip is not None:
                    # To check if the_tip is not None
                    the_tip = f" {self.user_improvements[key][tip]}"
                    if the_tip != "" and the_tip != " ":
                        print(f"- {self.user_improvements[key][tip]}")

    # TODO: Add more categories and tips. Improve user interface in general