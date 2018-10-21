from flask import render_template, Blueprint, jsonify
from catalog_app.models import Item, Category

core = Blueprint('core', __name__)


# This is the main page
@core.route('/')
def index():

    # get latest 5 products
    items = Item.query.order_by(Item.id.desc()).limit(5).all()
    categories = Category.query.all()
    return render_template('index.html', items=items, categories=categories)


# Return all items in all categories as a JSON API
@core.route("/catalog.json")
def json_all():

    categories = Category.query.all()
    return jsonify(categories=[category.serialize for category in categories])

