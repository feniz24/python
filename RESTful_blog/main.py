from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime
import nh3

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField('Body')
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:id>")
def show_post(id):
    requested_post = BlogPost.query.get(id)
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        with app.app_context():
            title = form.title.data
            subtitle = form.subtitle.data
            author = form.author.data
            img_url = form.img_url.data
            body = form.body.data
            clean_body = nh3.clean(body, tags=nh3.ALLOWED_TAGS)
            date = datetime.datetime.now().strftime("%B %d, %Y")
            new_post = BlogPost(title=title, subtitle=subtitle, author=author, img_url=img_url, body=clean_body, date=date)
            db.session.add(new_post)
            db.session.commit()
        return redirect('/')

    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post_update = db.session.query(BlogPost).get(post_id)
    edit_form = CreatePostForm(
        title=post_update.title,
        subtitle=post_update.subtitle,
        img_url=post_update.img_url,
        author=post_update.author,
        body=post_update.body
    )
    if edit_form.validate_on_submit():
        post_update.title = edit_form.title.data
        post_update.subtitle = edit_form.subtitle.data
        post_update.author = edit_form.author.data
        post_update.img_url = edit_form.img_url.data
        post_update.body = edit_form.body.data
        clean_body = nh3.clean(post_update.body, tags=nh3.ALLOWED_TAGS)
        post_update.body = clean_body
        db.session.commit()
        return redirect(url_for("show_post", id=post_update.id))

    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_delete = db.session.query(BlogPost).get(post_id)
    db.session.delete(post_delete)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
