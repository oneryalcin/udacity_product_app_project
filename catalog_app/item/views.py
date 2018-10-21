from flask import render_template, url_for, redirect, jsonify, Blueprint
from flask_login import login_required
from catalog_app import db
from catalog_app.item.forms import AddEditForm, DeleteForm
from catalog_app.models import Item, Category

items = Blueprint('items', __name__, url_prefix='/catalog')


def category_item_match(category, item):
    """
        Helper function to ensure category-item.category matches
    """
    item_ = Item.query.filter_by(name=item).first()

    # Just make sure item is in the correct category
    assert item_.category.name == category, \
        "item {} category is not in correct category " \
        "of {}".format(item_.name, category)

    return item_.category, item_


# item page displays item details
@items.route('/<category>/<item>')
def main(category, item):

    category_, item_ = category_item_match(category, item)
    return render_template('item_main.html', item=item_, category=category_)


# Json API endpoint for the function above
@items.route('/<category>/<item>.json')
def main_json(category, item):

    category_, item_ = category_item_match(category, item)
    return jsonify(item=item_.serialize)


# Edit an item, make sure endpoint is protected against logged out users
@items.route('/<item>/edit', methods=['GET', 'POST'])
@login_required
def edit(item):

    item = Item.query.filter_by(name=item).first()

    # Here also set the category selected item if the request is get
    form = AddEditForm(category=item.category_id)

    # Only Post data if validation passes, otherwise display errors on page
    if form.validate_on_submit():
        item.name = form.title.data
        item.description = form.description.data
        item.category_id = int(form.category.data)
        db.session.commit()

        updated_cat = Category.query.filter_by(id=item.category_id).first()
        return redirect(url_for('items.main',
                                category=updated_cat.name,
                                item=item.name))

    # Edit page needs data to be filled in
    form.title.data = item.name
    form.description.data = item.description
    return render_template('item_edit.html', form=form, item=item)


# Add a new Item, protect endpoint
@items.route('/add', methods=['GET', 'POST'])
@login_required
def add():

    form = AddEditForm()

    # Make sure posted data is valid.
    if form.validate_on_submit():

        new_item = Item(category_id=int(form.category.data),
                        name=form.title.data,
                        description=form.description.data)

        db.session.add(new_item)
        db.session.commit()

        category = Category.query.filter_by(id=new_item.category_id).first()
        return redirect(url_for('items.main', category=category.name,
                                item=new_item.name))

    return render_template('item_add.html', form=form)


# Delete Item, ensure endpoint protected
@items.route('/<item>/delete', methods=['GET', 'POST'])
@login_required
def delete(item):

    item = Item.query.filter_by(name=item).first()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()

        return redirect(url_for('core.index'))

    return render_template('item_delete.html', form=form, item=item)
