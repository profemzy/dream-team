from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager


class Member(UserMixin, db.Model):
    """
        Creates an Employee Table
    """

    # Ensures table name will be plural of the model name
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='member', lazy=True)

    @property
    def password(self):
        """
         Prevents password from being accessed
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
            Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
            Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Member: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))


class Post(db.Model):
    """
        Create Department Table
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'),
                          nullable=False)

    def __repr__(self):
        return '<Post: {}>'.format(self.title)


class Role(db.Model):
    """
        Create Role Table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    members = db.relationship('Member', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
