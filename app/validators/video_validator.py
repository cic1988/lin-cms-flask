from lin import manager
from lin.forms import Form
from lin.exception import ParameterException

from wtforms import DateTimeField, PasswordField, FieldList, IntegerField, StringField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange


class NewCategory(Form):
    name = StringField(validators=[DataRequired(message='please enter category name')])
    description = StringField(validators=[Optional()])

class CategorySearchForm(Form):
    q = StringField(validators=[DataRequired(message='please enter search words')])

class VideoSearchForm(Form):
    q = StringField(validators=[Optional()], default='')
    c = StringField(validators=[Optional()], default='')

    def validate(self):
        if not self.q.data and not self.c.data:
            raise ParameterException(msg="please enter search words")
        else:
            return self

class CreateOrUpdateVideoForm(Form):
    title = StringField(validators=[DataRequired(message='title is can not be empty')])
    description =StringField(validators=[Optional()], default='')
    thumbnail = StringField(validators=[DataRequired(message='thumbnail is can not be empty')])
    url = StringField(validators=[DataRequired(message='url is can not be empty')])
    embedded = StringField(validators=[Optional()])
    category = StringField(validators=[Optional()], default='others')
    tags = StringField(validators=[Optional()], default='')
