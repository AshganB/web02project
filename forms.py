from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,TextAreaField,IntegerField,EmailField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Length,ValidationError,Email,EqualTo

#class SampleForm(FlaskForm):
    #userName = StringField('Your name', validators=[DataRequired(), Length(min=1, max=80)])

    #submit = SubmitField('Submit')


#new place insertionForm:

class insertionForm(FlaskForm):
    place=StringField(label="PlaceName", validators=[DataRequired()])
    latitude=IntegerField(label="Latitude")
    longitude=IntegerField(label="Longitude")
    submit=SubmitField("Send")

#RegisterationForm class:

class RegistrationForm(FlaskForm):
    fullname = StringField(
        'Full Name', 
        validators=
            [DataRequired(), 
            Length(min=2, max=200)
        ]
    )

    username = StringField(
        'Username / Display Name', 
        validators=
            [DataRequired(), 
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(), 
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Sign up')  

    # login form

    class LoginForm(FlaskForm):
      username = StringField(
        'Username / Display Name',
        validators=[
            DataRequired()
        ]
    )

      password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

      remember = BooleanField('Remember me')

      submit = SubmitField('Login')    