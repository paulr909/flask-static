from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    recaptcha = RecaptchaField()
    name = StringField(
        "Name", validators=[DataRequired(message="Please enter your name")]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Please enter your email address"),
        ],
    )
    industry = SelectField(
        "Industry",
        choices=[
            ("Media and Entertainment", "Media and Entertainment"),
            ("Finance", "Finance"),
            ("Travel", "Travel"),
            ("Engineering", "Engineering"),
            ("Healthcare", "Healthcare"),
            ("Other", "Other"),
        ],
    )
    message = TextAreaField(
        "Message", validators=[DataRequired(message="Please enter your message")]
    )
    submit = SubmitField("Send")
