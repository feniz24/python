from flask import Flask
import random

app = Flask(__name__)

random_num = random.randint(0, 9)


@app.route("/")
def home():
    return ("<h1>Guess a number between 0 and 9</h1>"
            "<img src='https://media.giphy.com/media/v1"
            ".Y2lkPTc5MGI3NjExOGM0cWR3djBzcXF2aHEyNzJzcjBxYzMyaDU1OTRxZW00aHIzeDh0MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7aCSPqXE5C6T8tBC/giphy.gif'>")


@app.route("/<int:number>")
def guess(number):
    if number > random_num:
        return "<h1>Too high. Try again</h1><img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>"
    elif number < random_num:
        return "<h1>Too low. Try again</h1><img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
    else:
        return "<h1>You found it</h1><img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>"


if __name__ == "__main__":
    app.run(debug=True)
