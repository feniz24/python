from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/all")
def all_cafe():
    cafes = db.session.query(Cafe).all()
    return jsonify({"cafes": [cafe.to_dict() for cafe in cafes]})


@app.route("/random", methods=["GET"])
def random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/search", methods=["GET"])
def search_cafe():
    location = request.args.get("loc")
    cafes = Cafe.query.filter_by(location=location).all()
    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={'Not Found': "Sorry. we don't have a cafe at that location"})


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    try:
        new_cafe = Cafe(
            name=request.form['name'],
            location=request.form['location'],
            seats=request.form['seats'],
            img_url=request.form['img_url'],
            map_url=request.form['map_url'],
            coffee_price=request.form['coffee_price'],
            has_wifi=bool(request.form['has_wifi']),
            has_toilet=bool(request.form['has_toilet']),
            has_sockets=bool(request.form['has_sockets']),
            can_take_calls=bool(request.form['can_take_calls']),
        )
    except KeyError:
        return jsonify(error={"Bad Request": "Some or all fields were incorrect or missing."})
    else:
        with app.app_context():
            db.session.add(new_cafe)
            db.session.commit()
        return jsonify(response={"success": f"Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["GET", "PATCH"])
def update_cafe(cafe_id):
    cafe_to_update = db.session.query(Cafe).get(cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = request.form.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price"}), 200
    else:
        return jsonify(error={"Not found": f"Sorry, a cafe with id {cafe_id} was not found in the database"}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecret":
        cafe_to_update = db.session.query(Cafe).get(cafe_id)
        if cafe_to_update:
            db.session.delete(cafe_to_update)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not found": f"Sorry, a cafe with id {cafe_id} was not found in the database"}), 404
    else:
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key."), 403


if __name__ == '__main__':
    app.run(debug=True)
