from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap


class MyForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log In', validators=[DataRequired()])


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app


app = create_app()
app.secret_key = "some secret string"


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = MyForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        if email == "admin@email.com" and password == "12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
