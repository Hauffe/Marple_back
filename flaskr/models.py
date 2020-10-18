from . import db
import json
from collections import namedtuple
from json import JSONEncoder

class Restriction:
    def __init__(self, enable, id, ingredients, name):
        self.enable, self.id, self.ingredients, self.name = enable, id, ingredients, name


class Ingredient:
    def __init__(self, description, id, name):
        self.description, self.id, self.name = description, id, name


class RestrictionEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class User(db.Model):
    """Data model for 'produtos'"""

    __tablename__ = 'user'
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String,
                         index=False,
                         unique=True,
                         nullable=False)
    password = db.Column(db.String,
                         nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)
