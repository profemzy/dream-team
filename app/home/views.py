from flask import render_template, abort
from flask_login import login_required, current_user
from sqlalchemy import desc

from app.models import Post
from . import home


@home.route('/')
def homepage():
    """
    Render t he home page template on the / route
    :return: render homepage template
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevents non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title='Dashboard')


@home.route('/dashboard')
@login_required
def dashboard():
    """
        Render the dashboard template on the /dashboard route
    :return: render dashboard template
    """
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/blog', methods=['GET', 'POST'])
def list_posts():
    """
    List All Posts
    :return:
    """
    posts = Post.query.order_by(desc('pub_date')).all()
    return render_template('home/posts.html',
                           posts=posts, title='Posts')


@home.route('/posts/read/<int:id>', methods=['GET', 'POST'])
def read_post(id):
    """
    Read a post
    :param id:
    :return:
    """

    post = Post.query.get_or_404(id)

    return render_template('home/post.html', post=post)
