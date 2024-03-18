from tkinter import *
import pandas as pd
import random as rd

BACKGROUND_COLOR = "#B1DDC6"
words = {}
try:
    data = pd.read_csv("./data/to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/french_words.csv")
    words = original_data.to_dict(orient="records")
else:
    words = data.to_dict(orient="records")

word = {}


def next_card():
    global word, timer
    word = rd.choice(words)
    window.after_cancel(timer)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=word["French"], fill="black")
    canvas.itemconfig(card_back, image=card_front_img)
    timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word["English"], fill="white")
    canvas.itemconfig(card_back, image=card_back_img)


def remove_card():
    words.remove(word)
    updated_data = pd.DataFrame(words)
    updated_data.to_csv("./data/to_learn.csv", index=False)
    next_card()


window = Tk()
window.title('Learn French the easy way')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_back = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_img, correct_img = PhotoImage(file="./images/wrong.png"), PhotoImage(file="./images/right.png")
wrong_button, correct_button = Button(image=wrong_img, command=next_card), Button(image=correct_img, command=remove_card)
wrong_button.grid(row=1, column=0)
correct_button.grid(row=1, column=1)

next_card()
window.mainloop()
