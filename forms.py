from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message=f"Enter a valid email.")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=35)])
    recaptcha = RecaptchaField()
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class TODOItemForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField("Todo item description")
    submit = SubmitField("Add")
    cancel = SubmitField("Cancel")
