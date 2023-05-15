from forms import UserLoginForm, UserRegistrationForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signin', methods = ['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))


    form = UserLoginForm()

    if form.validate_on_submit():
        logged_user = User.query.filter_by(email = form.email.data).first()

        if logged_user and check_password_hash(logged_user.password, form.password.data):
            login_user(logged_user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('site.home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')
    return render_template('sign_in.html', title = 'Sign In', form = form)


@auth.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))

    form = UserRegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        first_name = form.f_name.data
        last_name = form.l_name.data

        user = User(email, username, password, first_name = first_name, last_name = last_name)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.f_name.data} {form.l_name.data}! You are now able to log in', 'success')

        return redirect(url_for('site.home'))
    print('please help')
    return render_template('sign_up.html', title ='Sign Up', form = form)



@auth.route('/logout', methods =['GET'])
def logout():
    logout_user()
    return redirect(url_for('site.home'))