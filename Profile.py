from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
db = SQLAlchemy(app)

# User profile
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    homeAddress = db.Column(db.String(120), nullable=False)

# GET / see profile info
@app.route('/profile/<username>', methods=['GET'])
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            "username": user.username,
            "password": user.password,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "homeAddress": user.homeAddress
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404

# POST / create profile
@app.route('/admin/profile', methods=['POST'])
def create_profile():
    data = request.get_json()
    new_user = User(
        username = data['username'], 
        password = data['password'],
        firstName = data['firstName'],
        lastName = data['lastName'],
        email = data['email'],
        homeAddress = data['homeAddress']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully."}), 201

# PUT / change profile info
@app.route('/admin/profile/<username>', methods=['PUT'])
def update_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        user.firstName = data.get('firstName', user.firstName)
        user.lastName = data.get('lastName', user.lastName)
        user.email = data.get('email', user.email)
        user.homeAddress = data.get('homeAddress', user.homeAddress)
        db.session.commit()
        return jsonify({"message": "User updated successfully."}), 200
    else:
        return jsonify({"message": "User not found."}), 404
    
# Credit card
class CreditCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.String(16), unique=True, nullable=False)
    expirationDate = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('credit_cards', lazy=True))

# POST / create credit card
@app.route('/profile/<username>/creditcard', methods=['POST'])
def add_credit_card(username):
    user = User.query.filter_by(username=username).first()
    if user:
        data = request.get_json()
        new_card = CreditCard(
            cardNumber = data['cardNumber'],
            expirationDate = data['expirationDate'],
            cvv = data['cvv'],
            user_id = user.id
        )
        db.session.add(new_card)
        db.session.commit()
        return jsonify({"message": "Credit card added successfully."}), 201
    else:
        return jsonify({"message": "User not found."}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
