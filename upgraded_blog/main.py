from flask import Flask, render_template, request
import requests
import smtplib


app = Flask(__name__)
blog_api = "https://api.npoint.io/271ef9ccbbdb9eefc57f"

response = requests.get(blog_api)
all_posts = response.json()

my_email = ""
password = ""


@app.route("/")
def home():
    return render_template("index.html", posts=all_posts)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["username"]
        email = data["email"]
        phone = data["phone"]
        text = data["text"]
        send_email(name, email, phone, text)
        return render_template("contact.html", method="POST")
    return render_template("contact.html")


def send_email(name, email, phone, text):
    message = f"Subject:Blog Contact\n\n Name:{name}\n Email: {email}\n Phone: {phone}\n Message: {text}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg=message)
    return render_template("contact.html", method="POST")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/<int:num>")
def get_post(num):
    print(all_posts)
    blog_post = all_posts[num-1]
    # print(blog_post)
    return render_template("post.html", post=blog_post)


if __name__ == "__main__":
    app.run(debug=True)
