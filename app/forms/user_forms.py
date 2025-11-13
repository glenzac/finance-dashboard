"""Forms for user management."""
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, Regexp


class UserForm(FlaskForm):
    """Form for adding/editing users."""

    name = StringField(
        'User Name',
        validators=[
            DataRequired(message="User name is required"),
            Length(min=2, max=50, message="Name must be between 2 and 50 characters")
        ],
        render_kw={"placeholder": "Enter user name"}
    )

    email = EmailField(
        'Email',
        validators=[
            Optional(),
            Email(message="Invalid email address")
        ],
        render_kw={"placeholder": "user@example.com (optional)"}
    )

    color = StringField(
        'Color',
        validators=[
            DataRequired(message="Color is required"),
            Regexp(r'^#[0-9A-Fa-f]{6}$', message="Color must be in hex format (#RRGGBB)")
        ],
        default="#007bff",
        render_kw={"type": "color"}
    )

    is_active = BooleanField(
        'Active',
        default=True
    )

    submit = SubmitField('Save User')


class UserDeleteForm(FlaskForm):
    """Form for confirming user deletion."""

    submit = SubmitField('Confirm Delete')
