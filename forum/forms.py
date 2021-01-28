from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from forum.models import User

class registration_form(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])
    submit = SubmitField("sign up")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username already taken")

class login_form(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])
    submit = SubmitField("log in")

class topic_form(FlaskForm):
    header = StringField("title", validators = [DataRequired()])
    content = TextAreaField("content", validators = [DataRequired()])
    submit = SubmitField("post")