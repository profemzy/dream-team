from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from app.admin.forms import DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Employee


def check_admin():
    """
        Prevent non-admin from accessing the page
    :return:
    """
    if not current_user.is_admin:
        abort(403)


# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List All Departments
    :return:
    """
    check_admin()
    departments = Department.query.all()
    return render_template('admin/departments/departments.html',
                           departments=departments, title='Departments')


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a new department to the database
    :return:
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

        # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    :param id:
    :return:
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully updated the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html',
                           action="Edit", add_department=add_department,
                           form=form, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


# Role Views
@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    :return:
    """
    check_admin()
    add_role = True
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)

        try:
            # add role to database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role')
        except:
            # in case where role name already exist
            flash('Error: role name already exist')

        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Add Role")


@admin.route('/role/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
        Edit a Role
    :param id:
    :return:
    """
    check_admin()
    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully update the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
        List all employees
    :return:
    """
    check_admin()
    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title="Employees")


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
        Assign a department and role to an employee
    :return:
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned the employee a department and role')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form, title="Assign Employee")
