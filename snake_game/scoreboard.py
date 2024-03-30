from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 20, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.sety(270)
        self.score = 0
        with open("data.txt") as file:
            self.high_score = int(file.read())
        self.update()

    def update(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", move=False, align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.high_score:
            with open("data.txt", "w") as file:
                self.high_score = self.score
                file.write(str(self.high_score))
        self.score = 0
        self.update()

    def increase_score(self):
        self.score += 1
        self.update()
