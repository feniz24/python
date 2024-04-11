from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired
import requests

MOVIE_API = ''
API_READ_ACCESS = ''
app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={'expire_on_commit': False})
Bootstrap(app)

headers = {
            "accept": "application/json",
            "Authorization": ""
        }


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


# with app.app_context():
#     db.create_all()
#     new_movie = Movie(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )
#     db.session.add(new_movie)
#     db.session.commit()


class EditForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Log In', validators=[DataRequired()])


class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie', validators=[DataRequired()])


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    edit_form = EditForm()
    movie_id = request.args.get('id')
    movie_to_update = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar_one()

    if edit_form.validate_on_submit():
        movie_to_update.rating = float(edit_form.rating.data)
        movie_to_update.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    movie_selected = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar_one()
    return render_template("edit.html", movie=movie_selected, form=edit_form)


@app.route('/add', methods=['GET','POST'])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        title = add_form.title.data

        url = "https://api.themoviedb.org/3/search/movie"
        params = {"query": title}

        response = requests.get(url, headers=headers, params=params)
        all_movies = response.json()["results"]
        return render_template("select.html", movies=all_movies)
    return render_template("add.html", form=add_form)


@app.route('/select', methods=["POST", "GET"])
def select():
    movie_id = request.args.get('id')
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(movie_url, headers=headers)
    movie_data = response.json()
    title = movie_data["original_title"]
    img_url = f"https://image.tmdb.org/t/p/w500/{movie_data['poster_path']}"
    year = movie_data["release_date"].split("-")[0]
    description = movie_data["overview"]

    with app.app_context():
        new_movie = Movie(title=title, img_url=img_url, year=year, description=description)
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for("edit", id=new_movie.id))


@app.route("/delete", methods=["GET"])
def delete():
    movie_id = request.args.get('id')
    movie_to_update = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar_one()
    db.session.delete(movie_to_update)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)