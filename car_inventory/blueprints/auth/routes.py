# external imports

from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

# internal imports
from car_inventory.forms import RegisterForm, LoginForm
from car_inventory.models import User, db

# intiantate our auth blueprint 
auth = Blueprint('auth', __name__, template_folder='auth_templates')

# creating our sign up route/endpoint
@auth.route('/signup',methods=['GET', 'POST'])
# as soon as we hit the 'register' button changes method from GET to POST
def signup():

    # we need to instantiate our form
    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        # grab the input data from the form and save it to variables
        first_name = registerform.first_name.data
        last_name = registerform.last_name.data
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data
        print(email, password)
        
    # check the database for same username and/or email
    # Query the database

        if User.query.filter(User.username == username).first(): # if this comes back as something, the username already exists
            flash(' Username already exists. Please Try Again.', category='warning')
            return redirect('/signup')
    
        if User.query.filter(User.email == email).first():
            flash(' Email already exists. Please Try Again.', category='warning')
            return redirect('/signup')
    
        # instantiate a user object and commit to the db
        user = User(username, email,password, first_name=first_name, last_name=last_name)

        # add the user object to our database and commit the changes
        db.session.add(user)
        db.session.commit()

        flash (f" You have successfully registered user {username}", category='success')
        return redirect('/signin') # we will add signin here

    return render_template('sign_up.html', form=registerform)  


# sign in route 
@auth.route('/signin', methods = ['GET', 'POST'])
def signin():

    loginform = LoginForm()

    if request.method == 'POST' and loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data
        print(email, password)

        user = User.query.filter(User.email == email).first()
        print(user)

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f" {email} has been logged in successfully.", category ='success')
            return redirect('/')
        else:
            flash(f" Invalid email and/or password. Please try again.", category='warning')
            return redirect('/signin')
        
    return render_template('sign_in.html', form=loginform)


# sign out route
@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')