"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


from tokenize import String
from datetime import datetime
from xmlrpc.client import DateTime
from models import db, User, Message, Follows
from sqlite3 import IntegrityError
from app import app
import os
from unittest import TestCase

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_message_method(self):
        """Test that method creates message correctly"""
        # create user to send message
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # create message
        m = Message(text="test", user_id=u.id)
        db.session.add(m)
        db.session.commit()

        self.assertIsInstance(m.timestamp, datetime)
        self.assertIsInstance(m.text, str)

