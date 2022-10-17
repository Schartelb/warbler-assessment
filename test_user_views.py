"""Test View Routes"""

# run these tests like:
#
#    python -m unittest test_user_views.py
from flask import Flask, current_app, render_template, request, flash, redirect, session, g
from models import db, User, Message, Follows
from sqlite3 import IntegrityError
from app import CURR_USER_KEY, app
import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

    def test_logged_out_sites(self):
        """Check sites when logged out"""

        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h4>New to Warbler?</h4>", html)

        with app.test_client() as client:
            resp = client.get('/users/1/following', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<div class="alert alert-danger">Access unauthorized.</div>', html)

        with app.test_client() as client:
            resp = client.get('/users/1/followers', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<div class="alert alert-danger">Access unauthorized.</div>', html)

        with app.test_client() as client:
            resp = client.get('/users/profile', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<div class="alert alert-danger">Access unauthorized.</div>', html)

    def test_login(self):
        """Test User views after login"""
        with app.test_request_context():
            u1 = User.query.filter_by(username="testuser1").first()
            session[CURR_USER_KEY] = u1.id
            if CURR_USER_KEY in session:
                g.user = User.query.filter_by(
                    id=session[CURR_USER_KEY]).first()

        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{g.user.id}', html)

        # test_request_context allows to change g -> g.user seen as None object
        # g.user remains Nonetype object.  Not sure how to fix.
        # adding context to test_request_context seems correct method.
