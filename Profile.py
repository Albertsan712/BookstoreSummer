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

# GET profile info
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)