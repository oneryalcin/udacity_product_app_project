from catalog_app.models import Category
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


# I decided to use WTForms to have a better form handling
# Since both Add and Edit form structure is the same I'll use the class below
class AddEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    # Populate some categories
    try:
        choices = [(str(category.id), category.name)
                   for category in Category.query.all()]
    except Exception:
        choices = []
    category = SelectField('Category', choices=choices)

    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
