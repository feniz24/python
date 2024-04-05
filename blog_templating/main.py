from flask import Flask, render_template
from post import Post

app = Flask(__name__)
posts = Post()


@app.route('/')
def home():
    return render_template("index.html", posts=posts.get_post())


@app.route('/<int:num>')
def specific_post(num):
    return render_template("post.html", posts=posts.get_post(), num=num)


if __name__ == "__main__":
    app.run(debug=True)
