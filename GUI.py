from tkinter import *
from tkinter import messagebox

def img_bg():
    pass

def to_home():
    home_frame.pack(fill=BOTH, expand=True)


def to_food():
    home_frame.pack_forget()
    food_frame.pack(fill=BOTH, expand=True)


def exit_():
    exit_result = messagebox.askyesno(title="Exit", message="Are you sure you want to exit?")
    if exit_result:
        root.destroy()


root = Tk()

x = int(root.winfo_screenwidth() / 2 - 347)
root.geometry(f"694x700+{x}+0")

wf_image = PhotoImage(file='water footprint.png')

# HOME PAGE
home_frame = Frame(root)

food_btn = Button(home_frame, text='Food', command=to_food)
exit_btn = Button(home_frame, text='Exit', command=exit_)

home_canvas = Canvas(home_frame)
home_canvas.create_window(100, 40, anchor = "nw", window = food_btn)
home_canvas.create_window(100, 80, anchor = 'nw', window = exit_btn)

home_canvas.pack(fill=BOTH, expand=True)
home_frame.pack()


# FOOD FRAME
food_frame = Frame(root)
home_btn = Button(food_frame, text='Home', command=to_home)
root.mainloop()
