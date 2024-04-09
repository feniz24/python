from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, unique=True, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with app.app_context():
            new_book = Book(title=request.form.get("name"), author=request.form.get('author'),
                            rating=request.form.get('rating'))
            db.session.add(new_book)
            db.session.commit()
        return redirect('/')
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.session.execute(db.select(Book).filter_by(id=book_id)).scalar_one()
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", book=book_selected)


@app.route("/delete", methods=["GET"])
def delete():
    book_id = request.args.get('id')
    book_to_update = db.session.execute(db.select(Book).filter_by(id=book_id)).scalar_one()
    db.session.delete(book_to_update)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
