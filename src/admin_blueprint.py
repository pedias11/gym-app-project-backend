from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from src.user_model import User
from src.session_model import UserSessionItem
from werkzeug.security import check_password_hash
from flasgger import swag_from

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """
    Admin login.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.objects(email=email).first()
        if user and check_password_hash(user.password, password) and user.role == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash("Invalid credentials or not an admin", "error")
            return redirect(url_for('admin.admin_login'))
    return render_template('admin_login.html')


@admin_bp.route('/logout', methods=['POST'])
def admin_logout():
    """
    Admin logout.
    """
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin.admin_login'))  


@admin_bp.before_request
def restrict_to_admin():
    allowed_routes = ['admin.admin_login']
    if 'admin_logged_in' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('admin.admin_login'))  


@admin_bp.route('/')
def admin_dashboard():
    """
    Admin dashboard.
    """
    users = User.objects.all()
    sessions = UserSessionItem.objects.all()
    return render_template('admin_dashboard.html', users=users, sessions=sessions)


@admin_bp.route('/user/create', methods=['GET', 'POST'])
def create_user():
    """
    Create a new user.
    """
    if request.method == 'POST':
        new_user = User(
            firstname=request.form['firstname'],
            lastname=request.form['lastname'],
            email=request.form['email'],
            password=request.form['password'],
            subscription=request.form['subscription']
        )
        new_user.save()
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('create_user.html')


@admin_bp.route('/user/<string:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """
    Edit an existing user.
    """
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        user.email = request.form['email']
        user.subscription = request.form['subscription']
        user.update(firstname=user.firstname, lastname=user.lastname,email=user.email, subscription = user.subscription)
        user.reload()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('edit_user.html', user=user)


@admin_bp.route('/user/delete/<string:user_id>', methods=['POST'])
def delete_user(user_id):
    """
    Delete a user.
    """
    user = User.objects.get(id=user_id)
    user.delete()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/user_by_lastname', methods=['GET', 'POST'])
def search_user_by_lastname():
    """
    Search user(s) by lastname.
    """
    if request.method == 'POST':
        lastname = request.form['lastname']
        users = User.objects(lastname__icontains=lastname)
        return render_template('admin_dashboard.html', users=users, sessions=UserSessionItem.objects.all())
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/session/create', methods=['GET', 'POST'])
def create_session():
    """
    Create a new session.
    """
    if request.method == 'POST':
        new_session = UserSessionItem(
            email=request.form['email'],
            date=request.form['date'],
            time=request.form['time']
        )
        new_session.save()
        flash('Session created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('create_session.html')


@admin_bp.route('/session/<string:session_id>', methods=['GET', 'POST'])
def edit_session(session_id):
    """
    Edit an existing session.
    """
    session = UserSessionItem.objects.get(id=session_id)
    if request.method == 'POST':
        session.email = request.form['email']
        session.date = request.form['date']
        session.time = request.form['time']
        session.save()
        flash('Session updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('edit_session.html', session=session)


@admin_bp.route('/sessions_by_email', methods=['GET', 'POST'])
def get_sessions_by_email():
    """
    Get all the sessions for a specific user-email.
    """
    if request.method == 'POST':
        email = request.form['email']
        sessions = UserSessionItem.objects(email__icontains=email)
        return render_template('admin_dashboard.html', users=User.objects.all(), sessions=sessions)
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/sessions_by_date', methods=['GET', 'POST'])
def get_sessions_by_date():
    """
    Get the sessions for a specific date.
    """
    if request.method == 'POST':
        date = request.form['date']
        sessions = UserSessionItem.objects(date__icontains=date)
        return render_template('admin_dashboard.html', users=User.objects.all(), sessions=sessions)
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/session/delete/<string:session_id>', methods=['POST'])
def delete_session(session_id):
    """
    Delete a session.
    """
    session = UserSessionItem.objects.get(id=session_id)
    session.delete()
    flash('Session deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))
