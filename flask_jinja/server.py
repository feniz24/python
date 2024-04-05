from flask import Flask, render_template
import requests
import random
import datetime

app = Flask(__name__)

GENDER_ENDPOINT = "https://api.genderize.io"
AGE_ENDPOINT = "https://api.agify.io"


@app.route("/")
def hello():
    random_number = random.randint(1, 10)
    current_year = datetime.datetime.now().year
    return render_template("index.html", num=random_number, year=current_year, name="Feniz")


@app.route("/guess/<name>")
def guess(name):
    para = {
        "name": name
    }
    response = requests.get(AGE_ENDPOINT, params=para)
    data = response.json()
    age = data["age"]

    response = requests.get(GENDER_ENDPOINT, params=para)
    data = response.json()
    gender = data["gender"]

    return render_template("guess.html", name=name.title(), age=age, gender=gender)


@app.route("/blog/<num>")
def get_blog(num):
    print(num)
    blog_url = "https://api.npoint.io/271ef9ccbbdb9eefc57f"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
