from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import uuid 
from datetime import datetime


from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User (db.Model, UserMixin):

    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(150), unique = True, nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    cars = db.relationship('Car', back_populates = 'owner', lazy = 'subquery')

    def __init__(self, email, username, password, first_name = '', last_name ='', token =''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.username = username
        self.token = self.set_token(24)
    

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash
    
    def __repr__(self):
        return f'User {self.username} with {self.email} is IN DA HOUSE!!!!!'
    

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150), nullable = False)
    model = db.Column(db.String(150), nullable = False)
    year = db.Column(db.String(5), nullable = False)
    color = db.Column(db.String(150), nullable = True, default = '')
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    owner = db.relationship('User', back_populates ='cars')

    def __init__(self, make, model, year, user_token, color = '', id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.user_token = user_token
        self.color = color

    def __repr__(self):
        return f'The {self.year} {self.make} {self.model} has been added to your database'

    def set_id(self):
        return (secrets.token_urlsafe())
    
class CarSchema(ma.Schema):
    class Meta:
        fields  = ['id', 'make', 'model', 'year', 'color']

car_schema = CarSchema()
cars_schema = CarSchema(many = True)

