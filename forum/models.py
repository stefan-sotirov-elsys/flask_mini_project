from datetime import datetime
from forum import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    topics = db.relationship("Topic", backref = "author", lazy = True)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    header = db.Column(db.String(100), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

