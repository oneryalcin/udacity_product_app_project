from flask import render_template, jsonify, Blueprint
from catalog_app.models import Category

categories = Blueprint('catalog', __name__, url_prefix='/catalog')


# Main page for each category, lists items in this category
# and allows you to add items if logged in
@categories.route('/<category>/items')
def main(category):

    category = Category.query.filter_by(name=category).first()
    return render_template('category_main.html', category=category)


# JSON API endpoint for the endpoint above
@categories.route('/<category>/items.json')
def main_json(category):

    category = Category.query.filter_by(name=category).first()
    return jsonify(items=[item.serialize for item in category.items])



