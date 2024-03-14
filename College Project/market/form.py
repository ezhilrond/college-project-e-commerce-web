from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from market.model import User



class RegisterForm(FlaskForm):
	def validate_username(self, username_to_check):
		user= User.query.filter_by(username=username_to_check.data).first()
		if user:
			raise ValidationError("username already exists. Please try diff name..")
	def validate_email(self, email_to_check):
		email = User.query.filter_by(email_address=email_to_check.data).first()
		if email:
			raise ValidationError("Email already exists. Please try diff email address...")



	username= StringField(label="User Name:", validators=[Length(min=5, max=25), DataRequired()])
	email = StringField(label="Email: ", validators=[DataRequired()])
	#email= StringField(label="Email:", validators=[Email(), DataRequired()])
	password1= PasswordField(label="Password:",validators=[Length(min=5, max=8), DataRequired()])
	password2= PasswordField(label="Conform Password:",validators=[Length(min=5, max=8),EqualTo('password1'), DataRequired()])
	submit= SubmitField(label="Register")



class LoginForm(FlaskForm):
	username= StringField(label="User Name:", validators=[DataRequired()])
	password= PasswordField(label="Password:",validators=[DataRequired()])
	submit= SubmitField(label="Login")


class purchaseForm(FlaskForm):
	submit= SubmitField(label="purchase!")


class sellForm(FlaskForm):
	submit= SubmitField(label="sell!")
	
