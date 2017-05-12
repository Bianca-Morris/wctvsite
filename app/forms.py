from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField, SubmitField
import wtforms.validators as validators

class ContactForm(FlaskForm):
	name = StringField('name', [validators.Required("Please enter your name.")])
	email = StringField('email', [validators.Required("Please enter your email address."),validators.Email("That's not an email address!")])
	message = TextAreaField('message', [validators.Required("Please enter a message.")])
	submit = SubmitField('Send Message')