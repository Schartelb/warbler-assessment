"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import User, Message, Follows, Likes
import random

db.drop_all()
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

#generates sampling of likes based on expected number of users and messages
user_id = random.sample(range(300), 75)
message_id = random.sample(range(1000), 75)
like_list = [Likes(user_id=u, message_id=m)
             for u, m in zip(user_id, message_id)]
db.session.add_all(like_list)
db.session.commit()
