import unittest
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Member, Post, Role


class TestBase(TestCase):
    def create_app(self):
        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='postgresql://postgres:pwd.001@localhost:5432/pythonib_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        :return:
        """
        db.create_all()

        # create test admin user
        admin = Member(username="admin", password="admin2017", is_admin=True)

        # create non admin test user
        member = Member(username="test_user", password="test2017")

        # save users to database
        db.session.add(admin)
        db.session.add(member)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        :return:
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_member_model(self):
        """
        Test number of records in Members Table
        :return:
        """
        self.assertEqual(Member.query.count(), 2)

    def test_post_model(self):
        """
        Test number of records in the Posts Table
        :return:
        """

        # create post post
        post = Post(title="Test Title",
                    content="Test Content",
                    member_id=1)

        # save the post to the database
        db.session.add(post)
        db.session.commit()

        self.assertEqual(Post.query.count(), 1)

    def test_role_model(self):
        """
        Test number of records in Role Table
        :return:
        """

        # create test role
        role = Role(name="Head of Department",
                    description="Heads the Departmental Activities")

        # save role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)


class TestViews(TestBase):
    def test_homepage_view(self):
        """
        Test that the home page is accessible without login
        :return:
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        :return:
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is not accessible without login
        and redirects to login page and then logout
        :return:
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page and the dashboard
        :return:
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that admin dashboard in not accessible without login
        and redirects to login page and then to dashboard
        :return:
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_post_view(self):
        """
               Test that create posts page is inaccessible without login
               and redirects to login page then to posts page
        """
        target_url = url_for('admin.add_post')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_members_view(self):
        """
        Test that members page is inaccessible without login
        and redirects to login page then to members page
        """
        target_url = url_for('admin.list_members')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):
    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in str(response.data))

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in str(response.data))

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in str(response.data))


if __name__ == '__main__':
    unittest.main()
