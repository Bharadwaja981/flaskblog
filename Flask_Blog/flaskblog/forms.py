from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Details


class RegistrationForm(FlaskForm):
    firstname = StringField('firstname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('lastname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError('This email is already registered.')

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    collegeid = StringField('Collegeid', validators=[DataRequired()])
    def validate_collegeid(self, collegeid):
        user = User.query.filter_by(collegeid=collegeid.data).first()
        if user:
            raise ValidationError('This college Id is already registered.')
    profession = StringField('Profession', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    userloginid = StringField('userloginid',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class EditProfileForm(FlaskForm):
    intrest1 = StringField('I like it Most')
    intrest2 = StringField('My second preference')
    intrest3 = StringField('I am good at it')
    intrest4 = StringField('Not bad')
    intrest5 = StringField('ok ok')
    lnkdurl = StringField('Linkedin url')
    ghuburl = StringField('Github url')
    submit = SubmitField('Update')

class CreateProjectForm(FlaskForm):
    projecttitle = StringField('Project Title :')
    pmetadata = StringField('Project Meta data :', widget=TextArea())
    pdescription = StringField('Project description :', widget=TextArea())

class UpdateProjectForm(FlaskForm):
    projecttitle = StringField('Project Title :')
    pmetadata = StringField('Project Meta data :', widget=TextArea())
    pdescription = StringField('Project description :', widget=TextArea())