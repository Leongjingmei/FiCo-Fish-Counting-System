from ficoflask import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import redirect, url_for

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('register'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True)
    username= db.Column(db.String(20), unique =True, nullable =False)
    email= db.Column(db.String(50), unique =True, nullable =False)
    image_file= db.Column(db.String(100), nullable =False, default = "default.jpg")
    password = db.Column(db.String(60), nullable =False)
    date_created= db.Column(db.DateTime, default = datetime.utcnow)
    details = db.relationship('UserDetails', backref='parent', lazy=True)

    def __repr__(self):
        return f'{self.username}: {self.email} :{self.date_created.strftime("%d/%m/%d, %H:%M:%S")}'

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    firstname = db.Column(db.String(30), unique =True, nullable =False, default = "")
    lastname = db.Column(db.String(30), unique =True, nullable =False, default = "")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.firstname} {self.lastname}';

class Database(db.Model, UserMixin):
    result_id = db.Column(db.Integer, primary_key =True)
    image_file= db.Column(db.String(120), nullable =False, default = "default.jpg")
    detected_image= db.Column(db.String(120), nullable =False, default = "default.jpg")
    fish_count = db.Column(db.Integer, nullable =False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.result_id}: {self.user_id}: {self.detected_image}: {self.fish_count}';
