from app import app, db
from app.home import home
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request
from flask_mail import Message
from threading import Thread
from app.utils import send_async_email


@home.route('/')
@home.route('/index')
def index():
    return render_template('celis.html', title='Home', data_footer_aos="fade-left", data_aos_footer_delay=100, data_aos_header="fade-left", data_header_aos_delay=100)


@home.route('/mailform', methods=["POST"])
@login_required
def mailform():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    tel = request.form.get("tel")
    email = request.form.get("email")
    body_to_admins = request.form.get('feedback')
    message = "Thanks for contacting CELIS. We will reach out to you soon!"
    msg = Message('Your Issue/Request has been notified', sender="celis.students@gmail.com", recipients=[email])
    msg_admins = Message('Issue/Feedback/Request from' + email, sender="celis.students@gmail.com", recipients=['narayanadithya1234@gmail.com', 'aravindharinarayanan111@gmail.com'])
    msg.body = '''Your recent feedback/issue/request has been sent to our admins. Actions will be taken soon.'''
    msg_admins.body = "Hey you have a message from user {} {}".format(current_user.username, body_to_admins)
    Thread(target=send_async_email, args=(app, msg)).start()
    Thread(target=send_async_email, args=(app, msg_admins)).start()
    return redirect(url_for('home.index'))


@home.route('/basetemplate')
def base():
    return render_template('template.html', title='template')


@home.route('/contact')
@login_required
def contactus():
    return render_template('contactus.html', title='Contact Us')
