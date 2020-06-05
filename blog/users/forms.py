# forms for users
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from blog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')
    

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm Password',
                                 validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email is already registered!')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username is used by someone!')


class UpdateUserForm(FlaskForm):
    email = StringField('Update Email',
                        validators=[DataRequired(), Email()])
    username = StringField('Update Username',
                           validators=[DataRequired()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_email(self, field):
        if (User.query.filter_by(email=field.data).first() and
                field.data != current_user.email):
            raise ValidationError('Your email is already registered!')
    
    def validate_username(self, field):
        if (User.query.filter_by(username=field.data).first() and 
                field.data != current_user.username):
            raise ValidationError('Your username is used by someone!')
    
    