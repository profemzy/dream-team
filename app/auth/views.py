from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app.auth.forms import RegistrationForm, LoginForm
from . import auth
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
        Handles request to the /register route
        Adds an Employee to the database through the registration form
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login. ')

        # redirect to login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
        Handles requests to the /login route
        Logs in and employee through the login form
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        # checks whether employee exists in the database
        # checks if provided password matches that in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the appropriate dashboard page after login
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are invalid
        else:
            flash('INVALID EMAIL OR PASSWORD. ')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle request to the /logout route
    Log an employee out through the logout link
    :return:
    """
    logout_user()
    flash('You have successfully logged out. ')

    # redirect to the login page
    return redirect(url_for('auth.login'))
