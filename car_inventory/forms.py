# creating forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField
from wtforms.validators  import DataRequired, EqualTo, Email


# create out login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators = [DataRequired() ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# create our register form
class RegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators= [DataRequired() ])
    email = StringField('Email', validators = [DataRequired(), Email() ])
    password = PasswordField('Password', validators = [DataRequired()])
    verify_password = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# product form
class ProductForm(FlaskForm):
    name = StringField("Car Make and Model - Picture Search", validators =[DataRequired()])
    image = StringField("Img Url (Optional)")
    description = StringField("Description (Optional)")
    year = IntegerField("Year", validators =[DataRequired()])
    make = StringField("Car Make", validators =[DataRequired()])
    model = StringField("Car Model", validators =[DataRequired()])
    color = StringField("Color", validators =[DataRequired()])
    miles = IntegerField("Odometer Reading", validators =[DataRequired()])
    price = DecimalField("Cost", validators =[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField()