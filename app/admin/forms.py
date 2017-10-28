from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from ..models import Department, Role


class DepartmentForm(FlaskForm):
    """
        Form for admin to add or edit departments
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit roles
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign employee to Roles/Departments
    """''
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")

    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")

    submit = SubmitField('Submit')


