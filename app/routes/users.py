"""User management routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms.user_forms import UserForm, UserDeleteForm
from app.services.user_service import UserService

bp = Blueprint('users', __name__)
user_service = UserService()


@bp.route('/')
def index():
    """
    User management page - list all users.
    """
    users = user_service.get_all_users(active_only=False)
    active_count = user_service.get_user_count(active_only=True)
    total_count = user_service.get_user_count(active_only=False)

    return render_template(
        'users/list.html',
        users=users,
        active_count=active_count,
        total_count=total_count
    )


@bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add new user.
    """
    form = UserForm()

    if form.validate_on_submit():
        success, message, user_id = user_service.add_user(
            name=form.name.data,
            email=form.email.data if form.email.data else "",
            color=form.color.data
        )

        if success:
            flash(message, 'success')
            return redirect(url_for('users.index'))
        else:
            flash(message, 'danger')

    return render_template('users/add.html', form=form)


@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit(user_id):
    """
    Edit existing user.

    Args:
        user_id: User ID
    """
    user = user_service.get_user_by_id(user_id)

    if not user:
        flash(f'User with ID {user_id} not found', 'danger')
        return redirect(url_for('users.index'))

    form = UserForm(obj=type('obj', (object,), user)())

    if form.validate_on_submit():
        success, message = user_service.update_user(
            user_id=user_id,
            name=form.name.data,
            email=form.email.data if form.email.data else "",
            color=form.color.data,
            is_active=form.is_active.data
        )

        if success:
            flash(message, 'success')
            return redirect(url_for('users.index'))
        else:
            flash(message, 'danger')

    return render_template('users/edit.html', form=form, user=user)


@bp.route('/<int:user_id>/delete', methods=['POST'])
def delete(user_id):
    """
    Delete (deactivate) user.

    Args:
        user_id: User ID
    """
    # Don't allow deleting default user
    if user_id == 1:
        flash('Cannot delete the default user', 'danger')
        return redirect(url_for('users.index'))

    success, message = user_service.delete_user(user_id, soft_delete=True)

    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('users.index'))


@bp.route('/<int:user_id>/activate', methods=['POST'])
def activate(user_id):
    """
    Activate a deactivated user.

    Args:
        user_id: User ID
    """
    success, message = user_service.update_user(user_id, is_active=True)

    if success:
        flash(f'User activated successfully', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('users.index'))
