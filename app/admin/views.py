from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from datetime import datetime

from sqlalchemy import desc

from . import admin
from app.admin.forms import PostForm, RoleForm, MemberAssignForm
from .. import db
from ..models import Post, Role, Member


def check_admin():
    """
        Prevent non-admin from accessing the page
    :return:
    """
    if not current_user.is_admin:
        abort(403)


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


# Member Views

@admin.route('/members')
@login_required
def list_members():
    """
        List all members
    :return:
    """
    check_admin()
    members = Member.query.all()
    return render_template('admin/members/members.html',
                           members=members, title="Members")


@admin.route('/members/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_member(id):
    """
        Assign a role to a member
    :return:
    """
    check_admin()

    member = Member.query.get_or_404(id)

    # prevent admin from being assigned a role
    if member.is_admin:
        abort(403)

    form = MemberAssignForm(obj=member)
    if form.validate_on_submit():
        member.role = form.role.data
        db.session.add(member)
        db.session.commit()
        flash('You have successfully assigned the member a role')

        # redirect to the roles page
        return redirect(url_for('admin.list_members'))

    return render_template('admin/members/member.html',
                           member=member, form=form, title="Assign Member")


# Post Views

@admin.route('/posts', methods=['GET', 'POST'])
@login_required
def list_posts():
    """
    List All Posts
    :return:
    """
    check_admin()
    posts = Post.query.order_by(desc('pub_date')).all()
    return render_template('admin/posts/posts.html',
                           posts=posts, title='Posts')


@admin.route('/posts/add', methods=['GET', 'POST'])
@login_required
def add_post():
    """
    Add a new post to the database
    :return:
    """
    check_admin()

    add_post = True

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    member_id=current_user.id)
        try:
            # add post to the database
            db.session.add(post)
            db.session.commit()
            flash('You have successfully added a new post.')
        except:
            # in case post name already exists
            flash('Error: there was an error while creating post.')

        # redirect to posts page
        return redirect(url_for('admin.list_posts'))

        # load post template
    return render_template('admin/posts/post.html', action="Add",
                           add_post=add_post, form=form,
                           title="Add Post")


@admin.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    """
    Edit a post
    :param id:
    :return:
    """
    check_admin()

    add_post = False

    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.pub_date = datetime.utcnow
        post.member_id = current_user.id
        db.session.commit()
        flash('You have successfully updated the post.')

        # redirect to the posts page
        return redirect(url_for('admin.list_posts'))

    form.content.data = post.content
    form.title.data = post.title
    current_user.id = post.member_id
    return render_template('admin/posts/post.html',
                           action="Edit", add_post=add_post,
                           form=form, title="Edit Post")


@admin.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    """
    Delete a post from the database
    """
    check_admin()

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('You have successfully deleted the post.')

    # redirect to the posts page
    return redirect(url_for('admin.list_posts'))

    return render_template(title="Delete Post")
