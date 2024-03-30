from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
user_guess = screen.textinput(title="Make your Guess", prompt="Which turtle will win the race? Enter a color: ")

colors = ["red", "green", "purple", "orange", "blue", "yellow"]
all_turtles = []
pos = -160
for color in colors:
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(color)
    new_turtle.penup()
    pos = pos + 50
    new_turtle.goto(x=-235, y=pos)
    all_turtles.append(new_turtle)

if user_guess:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_guess:
                print(f"You've won! {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! {winning_color} turtle is the winner!")

        speed = random.randint(0,10)
        turtle.forward(speed)
screen.exitonclick()
