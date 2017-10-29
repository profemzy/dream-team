from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from ..models import Role


class PostForm(FlaskForm):
    """
        Form for admin to add or edit posts
    """
    title = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit roles
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MemberAssignForm(FlaskForm):
    """
    Form for admin to assign member to Roles
    """''

    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")

    submit = SubmitField('Submit')


