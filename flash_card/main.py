from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

new_word = {}

try:
    words = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_words = pd.read_csv("data/french_words.csv")
    to_learn = original_words.to_dict(orient="records")
else:
    to_learn = words.to_dict(orient="records")


# Generate new words
def next_card():
    global new_word, flip_timer
    window.after_cancel(flip_timer)
    new_word = random.choice(to_learn)
    canvas.itemconfig(title, text='French', fill="black")
    canvas.itemconfig(meaning, text=new_word['French'], fill="black")
    canvas.itemconfig(card, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


# Flip card
def flip_card():
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(meaning, text=new_word['English'], fill="white")


# Create words_list
def is_known():
    to_learn.remove(new_word)
    new_list = pd.DataFrame(to_learn)
    new_list.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
# Main Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
title = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
meaning = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))

# Buttons
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR,
                      command=next_card)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR,
                      command=is_known)
right_button.grid(row=1, column=1)

next_card()
window.mainloop()
