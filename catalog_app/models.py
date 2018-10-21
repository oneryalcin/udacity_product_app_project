from flask_login import UserMixin
from catalog_app import db, login_manager


@login_manager.user_loader
def load_user(userid):
    return User(userid)


# Very simple user model, We use Google Oauth and track user email
# for authentication in Flask-Login user id is user email
class User(UserMixin):
    def __init__(self, email):
        self.id = email

    def __repr__(self):
        return "User : {}".format(self.id)


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False, index=True)
    items = db.relationship('Item', backref='category', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Category Name: {}".format(self.name)

    # This method is used to populate JSON API
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'items': [item.serialize for item in self.items]
        }


class Item(db.Model):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, category_id, name, description):
        self.category_id = category_id
        self.name = name
        self.description = description

    def __repr__(self):
        return "Item(name={}, category_id={}, " \
               "description={})".format(self.name, self.category_id,
                                        self.description)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'category': self.category.name,
        }
