from flask import Flask

app = Flask(__name__)


def makebold(function):
    def wrapper():
        bold_text = f"<b>{function()}</b>"
        return bold_text

    return wrapper

def makeunderlined(function):
    def wrapper():
        bold_text = f"<u>{function()}</u>"
        return bold_text

    return wrapper


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/style")
@makebold
@makeunderlined
def style():
    return "Hello, Styled"


@app.route("/username/<name>")
def greet(name):
    return f"Hello, {name}"


if __name__ == "__main__":
    app.run(debug=True)
