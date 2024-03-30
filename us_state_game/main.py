import pandas as pd
import turtle

screen = turtle.Screen()
screen.title("U.S. States Game")

image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
game_is_on = True

states_data = pd.read_csv("50_states.csv")
states = states_data["state"].to_list()

correct_guess = []
score = 0

while game_is_on:
    answer_state = screen.textinput(title=f"{score}/50 Guess the State", prompt="What's another state's name?").title()

    if answer_state == "Exit":
        missing_state = [state for state in states if state not in correct_guess]
        new_data = pd.DataFrame(missing_state)
        new_data.to_csv("states.csv")
        break
    if answer_state in states:
        if answer_state not in correct_guess:
            t = turtle.Turtle()
            t.hideturtle()
            t.penup()
            state_x = int(states_data[states_data.state == answer_state].x)
            state_y = int(states_data[states_data.state == answer_state].y)
            t.setpos(state_x, state_y)
            t.write(answer_state)
            score += 1
            correct_guess.append(answer_state)