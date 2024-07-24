from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
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
@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.get_json()

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"message": f"User {data['username']} already has an account."}), 400
    
    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({"message": f"User {data['email']} already has an account."}), 400

    new_user = User(
        username=data['username'], 
        password=data['password'],
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        homeAddress=data['homeAddress']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"User {new_user.username} was created successfully."}), 201

# PUT / change profile info
@app.route('/profile/<username>', methods=['PUT'])
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
        return jsonify({"message": f"User {user.username} updated successfully."}), 200
    else:
        return jsonify({"message": "User not found."}), 404

# DELETE profile
@app.route('/profile/<username>', methods=['DELETE'])
def delete_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        CreditCard.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {username} was deleted successfully."}), 200
    else:
        return jsonify({"message": "User not found."}), 404


# Credit card
class CreditCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.String(16), nullable=False)
    expirationDate = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('credit_cards', lazy=True))

# GET credit card info
@app.route('/profile/<username>/creditcard/<cardNumber>', methods=['GET'])
def get_credit_card(username, cardNumber):
    user = User.query.filter_by(username=username).first()
    if user:
        card = CreditCard.query.filter_by(cardNumber=cardNumber, user_id=user.id).first()
        if card:
            return jsonify({
                "cardNumber": card.cardNumber,
                "expirationDate": card.expirationDate,
                "cvv": card.cvv
            }), 200
        else:
            return jsonify({"message": "Credit card not found."}), 404
    else:
        return jsonify({"message": "User not found."}), 404

# POST / create credit card
@app.route('/profile/<username>/creditcard', methods=['POST'])
def add_credit_card(username):
    user = User.query.filter_by(username=username).first()
    if user:
        data = request.get_json()
        new_card = CreditCard(
            cardNumber=data['cardNumber'],
            expirationDate=data['expirationDate'],
            cvv=data['cvv'],
            user_id=user.id
        )
        db.session.add(new_card)
        db.session.commit()
        return jsonify({"message": "Credit card added successfully."}), 201
    else:
        return jsonify({"message": "User not found."}), 404

# PUT / change credit info
@app.route('/profile/<username>/creditcard/<cardNumber>', methods=['PUT'])
def update_credit_card(username, cardNumber):
    user = User.query.filter_by(username=username).first()
    if user:
        card = CreditCard.query.filter_by(cardNumber=cardNumber, user_id=user.id).first()
        if card:
            data = request.get_json()
            card.cardNumber = data.get('cardNumber', card.cardNumber)
            card.expirationDate = data.get('expirationDate', card.expirationDate)
            card.cvv = data.get('cvv', card.cvv)
            db.session.commit()
            return jsonify({"message": "Credit card updated successfully."}), 200
        else:
            return jsonify({"message": "Credit card not found."}), 404
    else:
        return jsonify({"message": "User not found."}), 404

# DELETE credit card
@app.route('/profile/<username>/creditcard/<cardNumber>', methods=['DELETE'])
def delete_credit_card(username, cardNumber):
    user = User.query.filter_by(username=username).first()
    if user:
        card = CreditCard.query.filter_by(cardNumber=cardNumber, user_id=user.id).first()
        if card:
            db.session.delete(card)
            db.session.commit()
            return jsonify({"message": "Credit card deleted successfully."}), 200
        else:
            return jsonify({"message": "Credit card not found."}), 404
    else:
        return jsonify({"message": "User not found."}), 404


# GET / see info of all profiles & credit cards
@app.route('/admin/profiles', methods=['GET'])
def get_all_profiles():
    users = User.query.all()
    return jsonify([{
        "username": user.username,
        "password": user.password,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "homeAddress": user.homeAddress,
        "creditCards": [{
            "cardNumber": card.cardNumber,
            "expirationDate": card.expirationDate,
            "cvv": card.cvv
        } for card in user.credit_cards]
    } for user in users]), 200

# DELETE / delete all profiles & credit cards
@app.route('/admin/profiles/creditcards', methods=['DELETE'])
def delete_all_profiles_and_credit_cards():
    num_users_deleted = db.session.query(User).delete()
    num_cards_deleted = db.session.query(CreditCard).delete()
    db.session.commit()
    return jsonify({
        "message": f"Successfully deleted {num_users_deleted} users and {num_cards_deleted} credit cards."
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)