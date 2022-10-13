"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from sqlite3 import IntegrityError
from app import app
import os
from unittest import TestCase
from psycopg2.errors import UniqueViolation

from models import db, User, Message, Follows

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


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        repr_resp = u.__repr__()
        self.assertIn(u.username, repr_resp)

    def test_following_followed(self):
        """Does is_following/is_followed_by work?"""

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

        # Check for follows
        self.assertEqual(u2.is_following(u1), 0)
        self.assertEqual(u1.is_followed_by(u2), 0)
        self.assertEqual(u1.is_following(u2), 0)
        self.assertEqual(u2.is_followed_by(u1), 0)

        # Users both follow one another
        u2.following.append(u1)
        u1.following.append(u2)
        db.session.commit()

        # u1 should have 1 follower, and u2 should have 1 following
        self.assertEqual(u2.is_following(u1), 1)
        self.assertEqual(u1.is_followed_by(u2), 1)
        self.assertEqual(u1.is_following(u2), 1)
        self.assertEqual(u2.is_followed_by(u1), 1)

    def test_User_create_authenticate(self):
        """Does User.create work//fail under correct circumstances?"""
        # Does User.signup work with unique values
        u1 = User.signup(username="NewUser",
                         email="TestUser@test.com", password="HASH_PASS", image_url="jpeg.jpg")
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.username, "NewUser")

        # Does User.signup fail with repeated values
        u2 = User.signup(username="NewUser",
                         email="TestUser2@test.com", password="HASH_PASS", image_url="jpeg.jpg")
        db.session.add(u2)
        self.assertRaises(UniqueViolation, db.session.commit())
