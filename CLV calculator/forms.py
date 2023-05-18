from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class clvData(FlaskForm): 
    email = StringField('Email', validators=[DataRequired()])
    apiKey = PasswordField('Private API Key', validators=[DataRequired(),Length(min=30, max=40)])
    clvThreshold = IntegerField('CLV Group Size', validators=[NumberRange(min=1, max=100, message='Must be a number between 1 and 100')])
    submit = SubmitField('Calculate')